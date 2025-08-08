#!/usr/bin/env python3
"""
Simple example using the exact format provided
"""

import openai

# Replace with the API key provided to you
API_KEY = "<api-key>"

# Initialize the client
client = openai.OpenAI(
    api_key=API_KEY,
    base_url="https://agent.dev.hyperverge.org"
)

# Make a request
response = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "what is 2+2 ?"
        }
    ]
)

print("Response:")
print(response)
print("\nResponse content:")
print(response.choices[0].message.content)
