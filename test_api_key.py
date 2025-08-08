#!/usr/bin/env python3
"""
Test script to demonstrate OpenAI API usage with the provided API key
"""

from app.openai_client import initialize_client, chat_with_openai
import os

def test_openai_api():
    """
    Test the OpenAI API with the provided credentials
    """
    # Check if API key is set in environment
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key or api_key == "your_openai_api_key_here":
        print("❌ No API key found!")
        print("Please create a .env file in the assessment-backend directory with:")
        print("OPENAI_API_KEY=your_actual_api_key_here")
        print("\nOr set the environment variable:")
        print("set OPENAI_API_KEY=your_actual_api_key_here")
        return
    
    try:
        # Initialize the client with your API key
        print("Initializing OpenAI client...")
        initialize_client(api_key=api_key)
        print("✅ Client initialized successfully!")
        
        # Test with a simple question
        print("\nTesting API with a simple question...")
        response = chat_with_openai("what is 2+2?")
        print(f"✅ Response: {response}")
        
        # Test with a more complex question
        print("\nTesting API with a more complex question...")
        response = chat_with_openai("Explain quantum computing in simple terms")
        print(f"✅ Response: {response}")
        
        print("\n🎉 All tests passed! Your API key is working correctly.")
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("Please make sure to set your actual API key in the .env file.")
    except Exception as e:
        print(f"❌ API error: {e}")
        print("This might be due to:")
        print("- Invalid API key")
        print("- Network connectivity issues")
        print("- API service being down")

if __name__ == "__main__":
    test_openai_api()
