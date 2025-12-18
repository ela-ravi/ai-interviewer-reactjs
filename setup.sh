#!/bin/bash

echo "🚀 Setting up AI Interviewer..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env 2>/dev/null || echo "OPENROUTER_API_KEY=your_openrouter_api_key_here" > .env
    echo "⚠️  Please edit .env file and add your OpenRouter API key!"
    echo "💡 Get your key from: https://openrouter.ai/keys"
    echo ""
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Get your OpenRouter API key from: https://openrouter.ai/keys"
echo "2. Edit .env file and add your OpenRouter API key"
echo "3. Run: streamlit run app.py"
echo ""

