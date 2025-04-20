# Video Generation Pipeline

## Installation Guide
### 1. Clone repository from Github
```
git clone git@github.com:theanh-ktmt/genai-video-pipeline.git
```

### 2. Install dependencies
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Prepare API Keys
You have to get your API key set up to enable the application to connect to the Gemini service. Here's how:

- **Get your Gemini API key:** Go to https://aistudio.google.com/prompts/new_chat, sign in/up, and create a new API key. Copy it.
- **Set up your environment file:**
    - Copy `src/configs/.env.example` to `.env`.
    - Open `.env` and update the Gemini API key line with the key you copied.

## Launch Server
- Run server using this scripts
```
bash scripts/launch_server.sh
```
- Run client (*Doing...*)