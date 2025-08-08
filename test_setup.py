#!/usr/bin/env python3
"""
Simple test script to verify backend setup
"""

import os
import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn imported successfully")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False
    
    try:
        import openai
        print("✅ OpenAI imported successfully")
    except ImportError as e:
        print(f"❌ OpenAI import failed: {e}")
        return False
    
    try:
        import pydantic
        print("✅ Pydantic imported successfully")
    except ImportError as e:
        print(f"❌ Pydantic import failed: {e}")
        return False
    
    return True

def test_openai_key():
    """Test if OpenAI API key is set"""
    print("\nTesting OpenAI API key...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("✅ OpenAI API key is set")
        return True
    else:
        print("⚠️  OpenAI API key is not set")
        print("Please create a .env file with: OPENAI_API_KEY=your_api_key_here")
        return False

def test_app_import():
    """Test if the app can be imported"""
    print("\nTesting app import...")
    
    try:
        from app.main import app
        print("✅ App imported successfully")
        return True
    except ImportError as e:
        print(f"❌ App import failed: {e}")
        return False

def main():
    print("🔧 Backend Setup Test")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import test failed. Please install dependencies:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # Test OpenAI key
    test_openai_key()
    
    # Test app import
    if not test_app_import():
        print("\n❌ App import failed. Check your app structure.")
        sys.exit(1)
    
    print("\n✅ All tests passed! Your backend is ready to run.")
    print("\nTo start the server, run:")
    print("python start.py")

if __name__ == "__main__":
    main()
