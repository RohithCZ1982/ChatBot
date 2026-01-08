"""
Real Estate Chatbot for Land Developer
Built with LlamaIndex RAG, OpenAI GPT-4o, and Streamlit
"""

import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path

# LlamaIndex imports
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.agent import ReActAgent

# Load environment variables
load_dotenv()

# Configure OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("⚠️ Please set OPENAI_API_KEY in your .env file")
    st.stop()

# Initialize LlamaIndex settings
Settings.llm = OpenAI(model="gpt-4o", temperature=0.1, api_key=OPENAI_API_KEY)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small", api_key=OPENAI_API_KEY)


def load_plots_data():
    """
    Load the plots CSV data into a pandas DataFrame.
    Returns the DataFrame for querying.
    """
    csv_path = Path("data/plots.csv")
    if not csv_path.exists():
        st.error(f"❌ plots.csv not found at {csv_path}")
        return pd.DataFrame()
    
    try:
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        st.error(f"❌ Error loading plots.csv: {str(e)}")
        return pd.DataFrame()


def query_plots(
    plot_id: str = None,
    status: str = None,
    min_price: float = None,
    max_price: float = None,
    facing: str = None,
    available_only: bool = False
) -> str:
    """
    Query the plots CSV data to find plot information.
    
    Args:
        plot_id: Specific Plot ID to look up (e.g., "PLT-001")
        status: Filter by status (Available, Sold, Reserved)
        min_price: Minimum price filter
        max_price: Maximum price filter
        facing: Filter by facing direction (North, South, East, West)
        available_only: If True, only return available plots
    
    Returns:
        A formatted string with plot information
    """
    df = load_plots_data()
    
    if df.empty:
        return "❌ No plot data available. Please check if plots.csv exists."
    
    # Start with all plots
    filtered_df = df.copy()
    
    # Apply filters
    if plot_id:
        filtered_df = filtered_df[filtered_df["Plot_ID"].str.upper() == plot_id.upper()]
        if filtered_df.empty:
            return f"❌ Plot ID '{plot_id}' not found. Available Plot IDs: {', '.join(df['Plot_ID'].tolist())}"
    
    if status:
        filtered_df = filtered_df[filtered_df["Status"].str.lower() == status.lower()]
    
    if available_only:
        filtered_df = filtered_df[filtered_df["Status"].str.lower() == "available"]
    
    if min_price is not None:
        filtered_df = filtered_df[filtered_df["Price"] >= min_price]
    
    if max_price is not None:
        filtered_df = filtered_df[filtered_df["Price"] <= max_price]
    
    if facing:
        filtered_df = filtered_df[filtered_df["Facing"].str.lower() == facing.lower()]
    
    if filtered_df.empty:
        return "❌ No plots found matching your criteria."
    
    # Format the results
    result_lines = []
    result_lines.append(f"📊 Found {len(filtered_df)} plot(s):\n")
    
    for _, row in filtered_df.iterrows():
        price_formatted = f"₹{row['Price']:,.0f}"
        result_lines.append(
            f"• Plot ID: {row['Plot_ID']}\n"
            f"  - Area: {row['Area_SqFt']} sq.ft\n"
            f"  - Price: {price_formatted}\n"
            f"  - Status: {row['Status']}\n"
            f"  - Facing: {row['Facing']}\n"
        )
    
    return "\n".join(result_lines)


@st.cache_resource
def initialize_rag_engine():
    """
    Initialize the RAG engine with PDF documents and create the vector index.
    This function is cached to prevent reloading on every interaction.
    """
    data_dir = Path("data")
    pdf_dir = data_dir / "pdfs"
    
    # Create pdfs directory if it doesn't exist
    pdf_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if PDFs exist
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        st.warning(
            f"⚠️ No PDF files found in {pdf_dir}. "
            "Please add PDF brochures to the data/pdfs folder for document-based queries."
        )
        # Return None if no PDFs, agent will still work with CSV tool
        return None, None
    
    try:
        # Load PDF documents
        documents = SimpleDirectoryReader(str(pdf_dir)).load_data()
        
        # Create vector index
        index = VectorStoreIndex.from_documents(documents)
        
        # Create query engine
        query_engine = index.as_query_engine(similarity_top_k=3)
        
        return index, query_engine
    
    except Exception as e:
        st.error(f"❌ Error initializing RAG engine: {str(e)}")
        return None, None


@st.cache_resource
def initialize_agent(_query_engine):
    """
    Initialize the ReActAgent with tools for both PDF queries and CSV queries.
    This function is cached to prevent reloading on every interaction.
    """
    # System prompt for the agent
    system_prompt = (
        "You are a friendly Sales Consultant for a premium Land Developer. "
        "Answer questions about amenities, landscape, maintenance, and developer history "
        "using the brochure/document search tool. "
        "Check for plot availability, pricing, and details using the plot query tool. "
        "Always be polite and professional. "
        "If you use the CSV/plot tool, format the price nicely with currency symbols. "
        "If a plot is not found, suggest checking available plot IDs. "
        "Provide helpful and accurate information to assist potential buyers."
    )
    
    # Create the CSV query tool
    plots_tool = FunctionTool.from_defaults(
        fn=query_plots,
        name="query_plots",
        description=(
            "Query plot availability and pricing information from the plots database. "
            "Use this tool to: "
            "- Find plots by Plot ID (e.g., 'PLT-001') "
            "- Find available plots (use available_only=True) "
            "- Filter by status (Available, Sold, Reserved) "
            "- Filter by price range (min_price, max_price) "
            "- Filter by facing direction (North, South, East, West) "
            "Returns formatted plot information with ID, area, price, status, and facing."
        )
    )
    
    tools = [plots_tool]
    
    # Add PDF query tool if query engine is available
    if _query_engine is not None:
        from llama_index.core.tools import QueryEngineTool
        
        pdf_tool = QueryEngineTool.from_defaults(
            query_engine=_query_engine,
            name="brochure_search",
            description=(
                "Search through property brochures and documents for information about "
                "amenities, landscape features, maintenance policies, developer history, "
                "and general property information. Use this for questions about what the "
                "development offers, facilities, and background information."
            )
        )
        tools.append(pdf_tool)
    
    # Create the agent
    agent = ReActAgent.from_tools(
        tools=tools,
        llm=Settings.llm,
        system_prompt=system_prompt,
        verbose=True
    )
    
    return agent


def main():
    """Main Streamlit application"""
    
    # Page configuration
    st.set_page_config(
        page_title="Real Estate Chatbot",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Title and header
    st.title("🏠 Real Estate Chatbot")
    st.markdown("**Premium Land Developer - Sales Consultant**")
    st.markdown("Ask me about plots, pricing, amenities, and more!")
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Information")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", use_container_width=True, type="secondary"):
            st.session_state.messages = []
            st.session_state.processed_count = 0
            st.rerun()
        
        st.divider()
        
        st.markdown("""
        **Available Features:**
        - 📄 Query property brochures (amenities, landscape, etc.)
        - 📊 Check plot availability and pricing
        - 🔍 Search by Plot ID, status, price range, or facing
        
        **Sample Questions:**
        - "What plots are available?"
        - "Tell me about PLT-001"
        - "What amenities are available?"
        - "Show me plots under ₹1,500,000"
        """)
        
        st.divider()
        
        # Display current plots data
        st.subheader("📊 Current Plots Data")
        df = load_plots_data()
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("No plot data loaded")
        
        st.divider()
        
        # PDF upload section (optional)
        st.subheader("📄 Upload PDFs")
        uploaded_files = st.file_uploader(
            "Upload brochure PDFs",
            type=["pdf"],
            accept_multiple_files=True,
            help="Upload PDF files to add to the knowledge base"
        )
        
        if uploaded_files:
            pdf_dir = Path("data/pdfs")
            pdf_dir.mkdir(parents=True, exist_ok=True)
            
            for uploaded_file in uploaded_files:
                file_path = pdf_dir / uploaded_file.name
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            
            st.success(f"✅ Uploaded {len(uploaded_files)} file(s)")
            st.info("🔄 Please refresh the page to reload the RAG engine with new documents")
    
    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Initialize processed messages tracker
    if "processed_count" not in st.session_state:
        st.session_state.processed_count = 0
    
    # Initialize session state for agent (cached)
    if "agent" not in st.session_state:
        with st.spinner("🔄 Initializing RAG engine..."):
            index, query_engine = initialize_rag_engine()
            st.session_state.agent = initialize_agent(query_engine)
            st.session_state.query_engine = query_engine
    
    # Main chat container
    chat_container = st.container()
    
    with chat_container:
        # Display welcome message if no chat history
        if len(st.session_state.messages) == 0:
            st.markdown("---")
            st.markdown("### 👋 Welcome! How can I help you today?")
            st.markdown("""
            I can assist you with:
            - 📊 **Plot Availability** - Check which plots are available
            - 💰 **Pricing Information** - Get details on plot prices
            - 📄 **Property Details** - Learn about amenities and features
            - 🔍 **Custom Queries** - Ask me anything about the properties
            """)
            
            # Quick action buttons
            st.markdown("#### 💡 Quick Questions:")
            col1, col2 = st.columns(2)
            
            quick_prompt = None
            
            with col1:
                if st.button("📋 What plots are available?", use_container_width=True, key="btn_available"):
                    quick_prompt = "What plots are available?"
                if st.button("💰 Show me pricing", use_container_width=True, key="btn_pricing"):
                    quick_prompt = "Show me all plot prices"
            
            with col2:
                if st.button("🏠 Tell me about amenities", use_container_width=True, key="btn_amenities"):
                    quick_prompt = "What amenities are available?"
                if st.button("🔍 Find plots by price", use_container_width=True, key="btn_price_filter"):
                    quick_prompt = "Show me plots under ₹1,500,000"
            
            if quick_prompt:
                st.session_state.messages.append({"role": "user", "content": quick_prompt})
            
            st.markdown("---")
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input at the bottom
        if prompt := st.chat_input("💬 Ask me about plots, pricing, or amenities..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Process the latest user message if it hasn't been answered yet
        if (len(st.session_state.messages) > st.session_state.processed_count and
            st.session_state.messages[-1]["role"] == "user"):
            
            user_message = st.session_state.messages[-1]["content"]
            
            # Generate and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("🤔 Thinking..."):
                    try:
                        response = st.session_state.agent.chat(user_message)
                        st.markdown(str(response))
                        st.session_state.messages.append({"role": "assistant", "content": str(response)})
                        st.session_state.processed_count = len(st.session_state.messages)
                    except Exception as e:
                        error_msg = f"❌ Error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
                        st.session_state.processed_count = len(st.session_state.messages)


if __name__ == "__main__":
    main()
