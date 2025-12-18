"""
Quick test script to verify OpenRouter API configuration
"""
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()


async def test_openrouter_connection():
    """Test OpenRouter API connection with Mistral AI"""
    
    print("🔍 Testing OpenRouter API Configuration...\n")
    
    # Check API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in .env file")
        print("💡 Please create a .env file with your OpenRouter API key")
        print("\nExample:")
        print("OPENROUTER_API_KEY=your_key_here")
        return False
    
    if api_key == "your_openrouter_api_key_here":
        print("❌ Please replace 'your_openrouter_api_key_here' with your actual API key")
        print("💡 Get your key from: https://openrouter.ai/keys")
        return False
    
    print("✅ API key found in .env file")
    print(f"   Key starts with: {api_key[:10]}...")
    
    # Test API connection
    print("\n🔄 Testing connection to OpenRouter with Mistral AI...")
    
    try:
        from autogen_ext.models.openai import OpenAIChatCompletionClient
        from autogen_core.models import UserMessage
        
        client = OpenAIChatCompletionClient(
            model="mistralai/mistral-small-creative",
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
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

