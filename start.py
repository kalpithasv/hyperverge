import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY environment variable is not set!")
        print("Please set your OpenAI API key to use the AI features.")
        print("You can set it by creating a .env file with: OPENAI_API_KEY=your_api_key_here")
    
    # Run the FastAPI server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
