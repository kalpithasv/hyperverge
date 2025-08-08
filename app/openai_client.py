import openai
import os
import json
from typing import Dict, Any

# Global client variable
client = None

def initialize_client(api_key: str = None, base_url: str = "https://agent.dev.hyperverge.org"):
    """
    Initialize the OpenAI client with the provided API key and base URL
    """
    global client
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("API key is required. Please provide an API key or set OPENAI_API_KEY environment variable.")
    
    # For OpenAI v0.28.1
    openai.api_key = api_key
    openai.api_base = base_url
    client = openai
    return client

def chat_with_openai(prompt: str, model="openai/gpt-4o-mini", temperature=0.7, max_tokens=4000):
    """
    Send a prompt to OpenAI and return the response
    """
    global client
    if client is None:
        # Initialize client if not already done
        initialize_client()
    
    try:
        response = client.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")

def parse_json_response(response: str) -> Dict[str, Any]:
    """
    Parse JSON response from OpenAI, handling common formatting issues
    """
    try:
        if "```json" in response:
            start = response.find("```json") + 7
            end = response.find("```", start)
            json_str = response[start:end].strip()
        elif "```" in response:
            start = response.find("```") + 3
            end = response.find("```", start)
            json_str = response[start:end].strip()
        else:
            json_str = response.strip()
        
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON response: {str(e)}\nResponse: {response}")
