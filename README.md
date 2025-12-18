# AI Interviewer

An intelligent interview application powered by multi-agent AI system using Python Autogen, Mistral AI, and Streamlit.

## Features

- **Interactive Interview System**: Conduct technical interviews for various positions and technologies
- **Mistral AI Model**: Uses `mistralai/mistral-small-creative` via OpenRouter for intelligent responses
- **Multi-Agent Architecture**:
  - **Interviewer Agent**: Asks relevant technical questions one at a time
  - **User Proxy Agent**: Interfaces with the employee/interviewee
  - **Coach Agent**: Provides feedback on how to improve answers
  - **Scorer Agent**: Evaluates and scores each answer

## Setup

### Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your API key:**
   
   Create a `.env` file:
   ```bash
   OPENROUTER_API_KEY=your_api_key_here
   ```
   
   Get your key from: https://openrouter.ai/keys

3. **Test your setup (optional):**
   ```bash
   python test_api.py
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

📖 For detailed installation instructions, see [INSTALLATION.md](INSTALLATION.md)

## Usage

1. Enter the technology/domain (e.g., Python, JavaScript, Machine Learning)
2. Enter the position (e.g., Senior Developer, Data Scientist)
3. Click "Start Interview" to begin
4. Answer questions one at a time
5. Receive instant feedback and scoring for each answer
6. View your overall performance at the end

## Architecture

The application uses a multi-agent system where:
- The **Interviewer** generates contextual questions based on technology and position
- The **User Proxy** facilitates communication between the user and agents
- The **Coach** analyzes answers and provides improvement suggestions
- The **Scorer** evaluates answers on a scale and provides detailed feedback

## Requirements

- **Python 3.10+** (tested on 3.13)
- **OpenRouter API key** (for Mistral AI access)
- Internet connection

## Key Dependencies

- `autogen-agentchat==0.4.10` - Multi-agent framework
- `autogen-ext[openai]==0.4.10` - Model client extensions
- `streamlit==1.40.2` - Web interface
- `python-dotenv==1.0.1` - Environment management

## Model Information

This application uses **Mistral Small Creative** via OpenRouter:
- **Model**: `mistralai/mistral-small-creative`
- **Provider**: OpenRouter (https://openrouter.ai)
- **Features**: 
  - Excellent for conversational AI and creative tasks
  - Strong technical knowledge for interviews
  - Cost-effective compared to GPT-4
  - Fast response times

