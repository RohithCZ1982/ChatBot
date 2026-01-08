# Real Estate Chatbot - Land Developer RAG System

A sophisticated Real Estate Chatbot built with **LlamaIndex RAG**, **OpenAI GPT-4o**, and **Streamlit** for a premium Land Developer. The chatbot can answer questions about property amenities, plot availability, pricing, and more using both unstructured (PDF) and structured (CSV) data sources.

## 🚀 Features

- **Dual Data Sources:**
  - **Unstructured Data (PDFs):** Brochures containing information on amenities, landscape, maintenance, and developer history
  - **Structured Data (CSV):** Plot availability data with Plot_ID, Area_SqFt, Price, Status, and Facing

- **Intelligent Query System:**
  - Natural language queries about plots, pricing, and availability
  - Document search for amenities and property information
  - Filter plots by ID, status, price range, or facing direction

- **User-Friendly Interface:**
  - Clean Streamlit chat interface
  - Real-time plot data display
  - PDF upload functionality
  - Chat history maintained across sessions

## 📋 Prerequisites

- Python 3.10 or higher
- OpenAI API Key (GPT-4o access)

## 🛠️ Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd ChatBot
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Create a `.env` file in the project root
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```
   - **Don't have an API key?** See `HOW_TO_GET_API_KEY.md` for detailed instructions
   - Quick steps: Go to https://platform.openai.com/api-keys → Create new secret key

5. **Prepare data files:**
   - The `data/plots.csv` file is already created with sample data
   - Create a `data/pdfs/` folder and add your PDF brochures (optional, but recommended)

## 📁 Project Structure

```
ChatBot/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .env                  # Environment variables (create this)
└── data/
    ├── plots.csv         # Plot availability data
    └── pdfs/             # PDF brochures (create this folder)
```

## 🎯 Usage

### Option 1: Local Installation

1. **Start the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

2. **The app will open in your browser** (usually at `http://localhost:8501`)

3. **Try these sample questions:**
   - "What plots are available?"
   - "Tell me about PLT-001"
   - "Show me plots under ₹1,500,000"
   - "What amenities are available?" (requires PDFs in data/pdfs/)
   - "Find available plots facing North"

### Option 2: Google Colab

**Yes, you can run this in Google Colab!** 🎉

1. **Upload `run_in_colab.ipynb` to Google Colab**
2. **Follow the step-by-step cells** in the notebook
3. **Get a public URL** via ngrok to access your chatbot from anywhere
4. **See `COLAB_SETUP.md`** for detailed instructions

The Colab notebook includes:
- Automatic dependency installation
- Sample data generation
- File upload helpers
- ngrok tunnel setup for public access

## 📊 Sample Data

The `data/plots.csv` file contains 5 sample plots:
- PLT-001: 2500 sq.ft, ₹1,250,000, Available, North
- PLT-002: 3000 sq.ft, ₹1,500,000, Sold, East
- PLT-003: 2000 sq.ft, ₹1,000,000, Available, South
- PLT-004: 3500 sq.ft, ₹1,750,000, Available, West
- PLT-005: 2800 sq.ft, ₹1,400,000, Reserved, North

## 🔧 Configuration

### Adding PDF Documents

1. Place your PDF brochures in the `data/pdfs/` folder
2. The app will automatically index them on startup
3. You can also upload PDFs through the sidebar interface

### Modifying Plot Data

Edit `data/plots.csv` with your actual plot data. The CSV should have these columns:
- `Plot_ID`: Unique identifier (e.g., "PLT-001")
- `Area_SqFt`: Plot area in square feet
- `Price`: Price in your currency
- `Status`: Available, Sold, or Reserved
- `Facing`: Direction (North, South, East, West)

## 🧠 How It Works

1. **RAG Engine Initialization:**
   - PDFs are loaded and indexed using LlamaIndex's `VectorStoreIndex`
   - Creates embeddings for semantic search

2. **Agent Setup:**
   - Uses `ReActAgent` from LlamaIndex
   - Equipped with two tools:
     - **Brochure Search Tool:** Queries PDF documents
     - **Plot Query Tool:** Queries CSV data

3. **Query Processing:**
   - User asks a question
   - Agent decides which tool(s) to use
   - Results are formatted and returned to the user

## ⚠️ Troubleshooting

- **"OPENAI_API_KEY not found":** Make sure you've created a `.env` file with your API key
- **"No PDF files found":** This is okay if you only want to query plots. Add PDFs to `data/pdfs/` for document queries
- **Import errors:** Make sure all dependencies are installed: `pip install -r requirements.txt`

## 📝 Notes

- The RAG engine is cached using `@st.cache_resource` to prevent reloading on every interaction
- Chat history is maintained in Streamlit's session state
- Error handling is included for missing plots, files, and API issues

## 🔐 Security

- Never commit your `.env` file to version control
- Keep your OpenAI API key secure
- The `.env` file is already in `.gitignore` (if using git)

## 📚 Tech Stack

- **Python 3.10+**
- **Streamlit** - Chat UI
- **LlamaIndex** - RAG orchestration
- **OpenAI GPT-4o** - LLM
- **Pandas** - CSV data handling
- **python-dotenv** - Environment variable management

## 🤝 Contributing

Feel free to extend this chatbot with additional features like:
- Database integration for plots
- User authentication
- Conversation export
- Multi-language support

---

Built with ❤️ for premium Land Developers
