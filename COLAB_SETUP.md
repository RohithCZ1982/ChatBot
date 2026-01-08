# 🚀 Running in Google Colab

This guide will help you run the Real Estate Chatbot in Google Colab.

## Quick Start

1. **Open the notebook:**
   - Upload `run_in_colab.ipynb` to Google Colab, or
   - Copy the cells from the notebook into a new Colab notebook

2. **Run cells in order:**
   - Each cell sets up a part of the environment
   - Follow the instructions in each cell

3. **Get your public URL:**
   - After running the ngrok cell, you'll get a public URL
   - Click the URL to access your chatbot

## Detailed Steps

### Step 1: Install Dependencies
The first cell installs all required packages including `pyngrok` for exposing the app.

### Step 2: Set Up Project Structure
Creates the necessary directories (`data/pdfs`).

### Step 3: Create Sample Data
Generates the `plots.csv` file with sample plot data.

### Step 4: Set OpenAI API Key
**⚠️ IMPORTANT:** Replace `"your_openai_api_key_here"` with your actual OpenAI API key.

### Step 5: Upload app.py
You have two options:
- **Option A:** Upload the `app.py` file using the file uploader
- **Option B:** Copy-paste the entire `app.py` code into a new code cell

### Step 6: (Optional) Upload PDFs
Upload PDF brochures if you want to query document-based information.

### Step 7: Run Streamlit with ngrok
This cell:
- Starts an ngrok tunnel to expose your Streamlit app
- Provides a public URL you can access from anywhere
- Runs Streamlit in the background

### Step 8: Stop the App
When you're done, run this cell to:
- Stop the Streamlit process
- Close the ngrok tunnel

## Alternative: All-in-One Setup

If you prefer, you can create a single cell with all setup code:

```python
# Install dependencies
!pip install -q streamlit llama-index llama-index-llms-openai llama-index-embeddings-openai openai pandas python-dotenv pypdf pyngrok

# Setup
import os
from pathlib import Path
import pandas as pd
from pyngrok import ngrok
import subprocess

# Create directories
os.makedirs("data/pdfs", exist_ok=True)

# Create plots.csv
plots_data = {
    'Plot_ID': ['PLT-001', 'PLT-002', 'PLT-003', 'PLT-004', 'PLT-005'],
    'Area_SqFt': [2500, 3000, 2000, 3500, 2800],
    'Price': [1250000, 1500000, 1000000, 1750000, 1400000],
    'Status': ['Available', 'Sold', 'Available', 'Available', 'Reserved'],
    'Facing': ['North', 'East', 'South', 'West', 'North']
}
pd.DataFrame(plots_data).to_csv('data/plots.csv', index=False)

# Set API key (REPLACE WITH YOUR KEY)
OPENAI_API_KEY = "your_openai_api_key_here"
with open('.env', 'w') as f:
    f.write(f'OPENAI_API_KEY={OPENAI_API_KEY}')

# Upload app.py first, then:
# Start ngrok
port = 8501
public_url = ngrok.connect(port)
print(f"🌐 Public URL: {public_url}")

# Run Streamlit
!streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true > /dev/null 2>&1 &
```

## Important Notes

1. **API Key Security:**
   - Never share your Colab notebook with your API key visible
   - Consider using Colab's secrets manager for production

2. **Ngrok URL:**
   - The URL changes each time you restart ngrok
   - Free ngrok URLs are temporary (2 hours)
   - Keep the cell running to maintain the connection

3. **File Persistence:**
   - Files uploaded to Colab are temporary
   - Re-upload files if you restart the runtime

4. **Resource Limits:**
   - Colab has usage limits
   - Long-running sessions may be interrupted

## Troubleshooting

### Dependency Conflicts

If you see dependency conflict errors (like `jedi>=0.16` not installed):

1. **The notebook already includes the fix** - `jedi>=0.16` is installed first
2. **If issues persist**, try installing all packages together:
   ```python
   !pip install -q --upgrade pip jedi>=0.16 streamlit llama-index llama-index-llms-openai llama-index-embeddings-openai openai pandas python-dotenv pypdf pyngrok
   ```
3. **Ignore warnings** - Some dependency warnings are harmless and won't affect functionality

### Other Issues

- **"app.py not found":** Make sure you uploaded the file in Step 5
- **"Port already in use":** Run the stop cell first, then restart
- **"Ngrok connection failed":** Check your internet connection
- **"OpenAI API error":** Verify your API key is correct and has credits
- **"Import errors":** Restart the runtime (Runtime > Restart runtime) and run all cells again

## Using Colab Secrets (Recommended)

For better security, use Colab's secrets manager:

```python
from google.colab import userdata

# Set secret in Colab: Runtime > Manage secrets
OPENAI_API_KEY = userdata.get('OPENAI_API_KEY')

with open('.env', 'w') as f:
    f.write(f'OPENAI_API_KEY={OPENAI_API_KEY}')
```

This way, your API key won't be visible in the notebook code.

