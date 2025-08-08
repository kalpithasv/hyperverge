#!/usr/bin/env python3
"""
Simple API test script
"""

import requests
import json

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"✅ Health endpoint: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health endpoint failed: {e}")
        return False

def test_root_endpoint():
    """Test the root endpoint"""
    try:
        response = requests.get("http://localhost:8000/")
        print(f"✅ Root endpoint: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
        return False

def test_generate_endpoint():
    """Test the generate endpoint"""
    try:
        data = {
            "role": "Data Analyst",
            "skills": ["SQL", "Python"],
            "difficulty": "Beginner"
        }
        response = requests.post(
            "http://localhost:8000/generate",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ Generate endpoint: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Generated {result.get('total_questions', 0)} questions")
            print(f"Skills covered: {result.get('skills_covered', [])}")
        else:
            print(f"Error: {response.text}")
        return True
    except Exception as e:
        print(f"❌ Generate endpoint failed: {e}")
        return False

def main():
    print("🧪 Testing AI Assessment API")
    print("=" * 40)
    
    # Test basic endpoints
    health_ok = test_health_endpoint()
    root_ok = test_root_endpoint()
    
    if health_ok and root_ok:
        print("\n✅ Basic API is working!")
        
        # Test AI endpoint (requires OpenAI API key)
        print("\n🤖 Testing AI generation endpoint...")
        test_generate_endpoint()
    else:
        print("\n❌ Basic API tests failed")
    
    print("\n" + "=" * 40)
    print("Test completed!")

if __name__ == "__main__":
    main()
