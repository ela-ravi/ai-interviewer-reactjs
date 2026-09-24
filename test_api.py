"""
Quick test script to verify OpenRouter API configuration
"""
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()


async def test_openrouter_connection():
    """Test OpenRouter API connection with Mistral AI"""
    
    provider = os.getenv("LLM_PROVIDER") or "LLM"
    print(f"🔍 Testing {provider} API configuration...\n")
    
    api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("❌ LLM_API_KEY not found in .env file")
        print("💡 Set LLM_API_KEY, LLM_BASE_URL, and LLM_PROVIDER")
        return False
    
    print("✅ API key found in .env file")
    print(f"   Key starts with: {api_key[:10]}...")
    
    print(f"\n🔄 Testing connection to {provider}...")
    
    try:
        from autogen_ext.models.openai import OpenAIChatCompletionClient
        from autogen_core.models import UserMessage
        
        client = OpenAIChatCompletionClient(
            model=os.getenv("MODEL", "mistralai/mistral-small-2603"),
            api_key=api_key,
            base_url=os.getenv("LLM_BASE_URL") or os.getenv("OPENROUTER_BASE_URL") or "https://openrouter.ai/api/v1",
            model_info={
                "vision": False,
                "function_calling": True,
                "json_output": True,
                "family": "unknown",
            }
        )
        
        response = await client.create([
            UserMessage(content="Say 'Hello, I am Mistral AI!' in one sentence.", source="user")
        ])
        
        message = response.content
        
        print("✅ Connection successful!")
        print(f"\n📨 Test Response from Mistral AI:")
        print(f"   {message}")
        
        print(f"\n📊 Token Usage:")
        print(f"   Prompt tokens: {response.usage.prompt_tokens}")
        print(f"   Completion tokens: {response.usage.completion_tokens}")
        
        print("\n✨ Your setup is ready! You can now run:")
        print("   streamlit run app.py")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        print("\n💡 Please install the required packages:")
        print("   pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        print("\n💡 Common issues:")
        print("   1. Invalid API key - check your key at https://openrouter.ai/keys")
        print("   2. No credits - add credits at https://openrouter.ai/credits")
        print("   3. Network connection issue")
        print("   4. Packages not installed - run: pip install -r requirements.txt")
        return False


if __name__ == "__main__":
    asyncio.run(test_openrouter_connection())

