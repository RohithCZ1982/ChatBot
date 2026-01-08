# 🔧 Troubleshooting Guide

Common issues and solutions for the Real Estate Chatbot.

## ❌ Invalid API Key Error

**Error Message:**
```
'invalid_api_key', 'code': 'invalid_api_key'
```

### Solution Steps:

1. **Verify your API key is set:**
   - Make sure you replaced `"your_openai_api_key_here"` with your actual key
   - The key should be in quotes: `OPENAI_API_KEY = "sk-proj-..."`

2. **Check your API key format:**
   - Valid keys start with `sk-proj-` or `sk-`
   - Should be about 50+ characters long
   - No extra spaces or quotes inside the key

3. **Get a new API key:**
   - Go to: https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Copy the entire key immediately
   - Paste it in your code

4. **Verify the key is active:**
   - Check your OpenAI dashboard: https://platform.openai.com/account/billing
   - Make sure your account has credits/active payment method
   - Check if the key was revoked (create a new one if needed)

5. **Common mistakes:**
   - ❌ Forgot to replace the placeholder text
   - ❌ Extra spaces before/after the key
   - ❌ Missing quotes around the key
   - ❌ Using an old/revoked key
   - ❌ Copy-paste errors (missing characters)

### Example of Correct Format:

```python
# ✅ CORRECT
OPENAI_API_KEY = "sk-proj-abc123def456ghi789jkl012mno345pqr678stu901vwx"

# ❌ WRONG - Placeholder not replaced
OPENAI_API_KEY = "your_openai_api_key_here"

# ❌ WRONG - Missing quotes
OPENAI_API_KEY = sk-proj-abc123...

# ❌ WRONG - Extra spaces
OPENAI_API_KEY = " sk-proj-abc123... "
```

## ❌ Ngrok Authentication Error

**Error Message:**
```
PyngrokNgrokError: authentication failed
```

### Solution:
1. Sign up at: https://dashboard.ngrok.com/signup
2. Get authtoken: https://dashboard.ngrok.com/get-started/your-authtoken
3. Set it in Step 7 of the notebook

## ❌ Module Not Found Errors

**Error:** `ModuleNotFoundError: No module named '...'`

### Solution:
1. Restart the Colab runtime: Runtime → Restart runtime
2. Run Step 1 (Install Dependencies) again
3. Make sure all cells ran successfully

## ❌ App Not Loading

**Symptoms:** ngrok URL shows error or doesn't load

### Solution:
1. Wait 10-15 seconds after running Step 8
2. Check if Streamlit is running (run the check cell)
3. Restart: Run Step 9 (Stop), then Step 8 again
4. Check the Colab output for error messages

## ❌ Dependency Conflicts

**Error:** `jedi>=0.16` or similar dependency warnings

### Solution:
- The notebook already includes fixes for this
- Warnings are usually harmless
- If issues persist, restart runtime and run Step 1 again

## ❌ File Not Found Errors

**Error:** `app.py not found` or `plots.csv not found`

### Solution:
1. **For app.py:** Make sure you uploaded it in Step 5
2. **For plots.csv:** Run Step 3 to create it
3. Check file structure: Run `!ls -la` to see files

## ❌ Rate Limit Errors

**Error:** `rate_limit_exceeded`

### Solution:
- Wait a few minutes
- Check your OpenAI usage limits
- Consider upgrading your OpenAI plan

## ❌ Insufficient Quota

**Error:** `insufficient_quota`

### Solution:
1. Check billing: https://platform.openai.com/account/billing
2. Add payment method if needed
3. Check usage limits in dashboard

## 🔍 Debugging Tips

### Check Your API Key:
```python
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv("OPENAI_API_KEY")
print(f"Key starts with: {key[:10]}..." if key else "Key not found!")
print(f"Key length: {len(key) if key else 0}")
```

### Test OpenAI Connection:
```python
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
try:
    response = client.models.list()
    print("✅ API key is valid!")
except Exception as e:
    print(f"❌ Error: {e}")
```

### Check Streamlit Status:
```python
import subprocess
result = subprocess.run(['pgrep', '-f', 'streamlit'], capture_output=True, text=True)
print("Running" if result.stdout else "Not running")
```

## 📞 Still Having Issues?

1. **Check the error message carefully** - it usually tells you what's wrong
2. **Restart the Colab runtime** - Runtime → Restart runtime
3. **Run cells in order** - Don't skip steps
4. **Check OpenAI status** - https://status.openai.com
5. **Verify all credentials** - API keys, ngrok token, etc.

## ✅ Quick Checklist

Before running the app, make sure:
- [ ] Step 1: Dependencies installed
- [ ] Step 2: Directories created
- [ ] Step 3: plots.csv created
- [ ] Step 4: OpenAI API key set (NOT the placeholder)
- [ ] Step 5: app.py uploaded
- [ ] Step 6: PDFs uploaded (optional)
- [ ] Step 7: ngrok authtoken set
- [ ] Step 8: Streamlit started successfully

---

**Most common issue:** Forgetting to replace the API key placeholder! Always double-check Step 4.

