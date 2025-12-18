# OpenRouter + Mistral AI Setup Guide

## 🚀 Quick Start

### 1. Get Your OpenRouter API Key

1. Visit: **https://openrouter.ai/keys**
2. Sign up or log in
3. Create a new API key
4. Copy the key

### 2. Configure the Application

Create a `.env` file in the project root:

```bash
OPENROUTER_API_KEY=your_actual_api_key_here
```

### 3. Install and Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## 🤖 Model Information

**Model**: `mistralai/mistral-small-creative`
- **Provider**: OpenRouter
- **Capabilities**: 
  - Excellent for conversational AI
  - Strong technical knowledge
  - Creative and contextual responses
  - Cost-effective compared to GPT-4

## 💰 Pricing

Check current pricing at: https://openrouter.ai/models/mistralai/mistral-small-creative

Mistral Small is generally very cost-effective:
- Much cheaper than GPT-4
- Good balance of quality and cost
- Pay-as-you-go pricing

## 🔧 Configuration Options

You can customize the model in your `.env` file:

```bash
# Use a different model
MODEL=mistralai/mistral-medium

# Adjust creativity (0.0 to 1.0)
TEMPERATURE=0.7
```

### Available Mistral Models on OpenRouter:
- `mistralai/mistral-small-creative` (default, balanced)
- `mistralai/mistral-small` (more focused)
- `mistralai/mistral-medium` (more capable)
- `mistralai/mistral-large` (most powerful)

## 🔍 How It Works

The application uses OpenRouter as a gateway to access Mistral AI models:

1. **Your App** → Sends request to OpenRouter
2. **OpenRouter** → Routes to Mistral AI
3. **Mistral AI** → Processes and returns response
4. **OpenRouter** → Returns to your app

Benefits:
- ✅ Single API key for multiple models
- ✅ Unified billing
- ✅ Easy model switching
- ✅ Automatic failover

## 🛟 Troubleshooting

### "API Key not found"
- Make sure you created `.env` file in the project root
- Check that the key name is exactly: `OPENROUTER_API_KEY`
- No spaces around the `=` sign

### "Rate limit exceeded"
- Add credits to your OpenRouter account
- Visit: https://openrouter.ai/credits

### "Model not found"
- Verify the model name is correct
- Check available models: https://openrouter.ai/models

## 📚 Resources

- **OpenRouter Docs**: https://openrouter.ai/docs
- **Mistral AI Docs**: https://docs.mistral.ai/
- **Supported Models**: https://openrouter.ai/models

