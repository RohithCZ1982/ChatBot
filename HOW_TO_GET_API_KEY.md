# 🔑 How to Get Your OpenAI API Key

This guide will walk you through getting your OpenAI API key step-by-step.

## Step-by-Step Instructions

### Step 1: Visit OpenAI Platform
Go to the OpenAI API keys page:
**https://platform.openai.com/api-keys**

Or navigate manually:
1. Go to https://platform.openai.com
2. Click on your profile (top right)
3. Select **"API keys"** from the menu

### Step 2: Sign Up or Log In
- **New users:** Click "Sign up" to create an account
- **Existing users:** Click "Log in" with your credentials

### Step 3: Add Payment Method (Required)
⚠️ **Important:** OpenAI requires a payment method to use the API, even for free tier usage.

1. Go to: https://platform.openai.com/account/billing
2. Click **"Add payment method"**
3. Enter your credit card details
4. Don't worry - you can set usage limits to avoid unexpected charges

### Step 4: Create Your API Key
1. Go back to: https://platform.openai.com/api-keys
2. Click the **"Create new secret key"** button
3. Give it a name (e.g., "Real Estate Chatbot" or "Colab Project")
4. Click **"Create secret key"**

### Step 5: Copy Your Key
⚠️ **CRITICAL:** Copy the key immediately! You won't be able to see it again after closing the dialog.

The key will look like this:
```
sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Step 6: Use Your Key

#### For Local Installation:
Create a `.env` file in your project root:
```
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

#### For Google Colab:
Paste your key in Step 4 of the notebook:
```python
OPENAI_API_KEY = "sk-proj-your-actual-key-here"
```

## 💰 Pricing Information

OpenAI charges based on usage:
- **GPT-4o:** ~$2.50-$10 per 1M input tokens, ~$10-$30 per 1M output tokens
- **Text Embedding:** ~$0.10 per 1M tokens
- **Free tier:** Usually includes $5-18 in free credits for new accounts

**Tips to manage costs:**
- Set usage limits in your OpenAI dashboard
- Monitor your usage regularly
- Use GPT-3.5-turbo instead of GPT-4o if cost is a concern (modify `app.py`)

## 🔒 Security Best Practices

1. **Never share your API key:**
   - Don't post it on forums, GitHub, or social media
   - Don't include it in screenshots

2. **Use environment variables:**
   - Store keys in `.env` files (already in `.gitignore`)
   - Never commit keys to version control

3. **Rotate keys regularly:**
   - Create new keys and delete old ones periodically
   - Revoke compromised keys immediately

4. **Set usage limits:**
   - Go to: https://platform.openai.com/account/limits
   - Set monthly spending limits to prevent unexpected charges

## ❓ Troubleshooting

### "Invalid API Key"
- Check for extra spaces or quotes
- Make sure you copied the entire key
- Verify the key hasn't been revoked

### "Insufficient Quota"
- Check your billing status
- Verify payment method is active
- Check usage limits in dashboard

### "Rate Limit Exceeded"
- You're making too many requests too quickly
- Wait a few minutes and try again
- Consider upgrading your plan

## 🔗 Useful Links

- **API Keys Dashboard:** https://platform.openai.com/api-keys
- **Billing Dashboard:** https://platform.openai.com/account/billing
- **Usage Dashboard:** https://platform.openai.com/usage
- **Documentation:** https://platform.openai.com/docs
- **Pricing:** https://openai.com/pricing

## 📝 Quick Reference

**Your API key format:**
```
sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Where to use it:**
- `.env` file: `OPENAI_API_KEY=your-key-here`
- Colab notebook: `OPENAI_API_KEY = "your-key-here"`
- Direct code (not recommended): `api_key = "your-key-here"`

---

**Need help?** Check the OpenAI documentation or their support forum.

