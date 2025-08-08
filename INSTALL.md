# Installation Guide

## Quick Start (Recommended)

If you're experiencing disk space issues, follow these steps:

### 1. Free Up Disk Space
```bash
# Clear pip cache
pip cache purge

# Clear temporary files (Windows)
del /q %TEMP%\*

# Or on Linux/Mac
rm -rf /tmp/*
```

### 2. Install Dependencies (Simplified)
```bash
# Use the simplified requirements file
pip install -r requirements-simple.txt
```

### 3. Set Up Environment
Create a `.env` file in the `assessment-backend` directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Test Setup
```bash
python test_setup.py
```

### 5. Start the Server
```bash
python start.py
```

## Alternative Installation Methods

### Method 1: Use Conda (if available)
```bash
conda create -n assessment python=3.9
conda activate assessment
pip install -r requirements-simple.txt
```

### Method 2: Use Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
pip install -r requirements-simple.txt
```

### Method 3: Install Packages Individually
```bash
pip install fastapi==0.95.2
pip install uvicorn==0.22.0
pip install openai==0.28.1
pip install pydantic==1.10.12
pip install python-multipart==0.0.6
pip install python-dotenv==1.0.0
```

## Troubleshooting

### Disk Space Issues
- Clear pip cache: `pip cache purge`
- Use `requirements-simple.txt` instead of `requirements.txt`
- Install packages one by one to identify problematic ones

### Import Errors
- Make sure you're in the correct directory (`assessment-backend`)
- Check Python version (3.8+ required)
- Try using a virtual environment

### OpenAI API Issues
- Verify your API key is correct
- Check if you have sufficient credits
- Ensure the `.env` file is in the correct location

## Verification

After installation, run:
```bash
python test_setup.py
```

This will verify that all components are working correctly.
