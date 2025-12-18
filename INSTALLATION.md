# Installation Guide

## Prerequisites

- Python 3.10+ (tested with Python 3.13)
- pip package manager
- OpenRouter API key (get from https://openrouter.ai/keys)

## Step-by-Step Installation

### 1. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `streamlit==1.40.2` - Web frontend framework
- `autogen-agentchat==0.4.10` - Multi-agent framework
- `autogen-ext[openai]==0.4.10` - Extensions for model clients
- `python-dotenv==1.0.1` - Environment variable management

### 3. Configure API Key

Create a `.env` file in the project root:

```bash
# Create .env file
cat > .env << EOF
OPENROUTER_API_KEY=your_actual_api_key_here
EOF
```

Or manually create `.env` file with:
```
OPENROUTER_API_KEY=your_actual_api_key_here
```

**Get your API key from:** https://openrouter.ai/keys

### 4. Test Your Setup (Optional but Recommended)

```bash
python test_api.py
```

You should see:
```
🔍 Testing OpenRouter API Configuration...
✅ API key found in .env file
🔄 Testing connection to OpenRouter with Mistral AI...
✅ Connection successful!
📨 Test Response from Mistral AI:
   Hello, I am Mistral AI!
✨ Your setup is ready! You can now run:
   streamlit run app.py
```

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Troubleshooting

### Error: "OPENROUTER_API_KEY not found"
- Make sure you created the `.env` file in the project root
- Check that the file is named exactly `.env` (with the dot at the beginning)
- Verify the API key is set correctly

### Error: "No module named 'autogen_agentchat'"
- Make sure you installed dependencies: `pip install -r requirements.txt`
- Check you're using the virtual environment if you created one

### Error: "Connection failed"
- Verify your API key is valid at https://openrouter.ai/keys
- Check you have credits at https://openrouter.ai/credits
- Ensure you have internet connection

### Import Errors on Windows
If you encounter async/event loop errors on Windows, add this to the top of your script:
```python
import sys
import asyncio

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
```

## Quick Commands Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Test setup
python test_api.py

# Run application
streamlit run app.py

# Deactivate virtual environment (when done)
deactivate
```

## Need Help?

1. Check the [README.md](README.md) for usage instructions
2. Review [OPENROUTER_SETUP.md](OPENROUTER_SETUP.md) for OpenRouter details
3. Check OpenRouter documentation: https://openrouter.ai/docs
4. Verify AutoGen documentation: https://microsoft.github.io/autogen/

