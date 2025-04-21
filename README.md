# 🚀 Video Generation Pipeline 🚀
A powerful pipeline for generating videos from text prompts using Gemini 2.0 Flash and Mochi 1.0 Preview

**🌟 Key Features**
-  **Prompt Refinement** – Enhances input prompts using Gemini 2.0 Flash for better video generation.
-  **High-Quality Video Generation** – Powered by Mochi 1.0 Preview (10B model).
- **Mock Mode** – Test without GPU by disabling `--enhance-prompt`.
- **Scalable Client-Server Model** – Handles multiple requests efficiently.
- **Multi-GPU Support** – Distributes workload across multiple workers.
- **Smart Scheduling** – Queue-based processing for optimal resource utilization.
- **Request Batching** - Increased parallelism and minimal user impact.

## 🎥 Sample Generated Videos
- Sample generated videos are located at `videos/`.
- Listing CSV file is at `videos/_listing.csv`, which contains:
    - Original prompts and Refined prompts
    - Generated video paths


## 🛠 Installation Guide
### 1️⃣ Clone the Repository
```
git clone git@github.com:theanh-ktmt/genai-video-pipeline.git
cd genai-video-pipeline
```

### 2️⃣ Set Up Virtual Environment & Install Dependencies
```
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows (if using CMD/PowerShell)
pip install -r requirements.txt
```

### 3️⃣ Configure API Keys

🔑 Gemini API Key Required
- Get your key from [Google AI Studio](https://aistudio.google.com/prompts/new_chat).
- Copy `.env.example` to `.env` and update:
```
GEMINI_API_KEY="your-api-key-here"
```

### 4️⃣ Login to HuggingFace (Required for Mochi)
```
huggingface-cli login
```
*(Enter your HuggingFace token when prompted.)*

### 5️⃣ Run Tests (Optional but Recommended)
```
# test AI tools
python tests/test_gemini.py
python tests/test_mochi.py

# for load test, server should run with --parallel-size and --max-batch-size larger than 1
python tests/test_load.py 
```

## 🚀 Launching the Server
### Default Mode (GPU Required)
*(Requires ~28GB VRAM for Mochi 1.0 Preview)*
```
bash scripts/launch_server_default.sh
```

### Mock Mode (No GPU Needed)
*(Disables video generation for quick testing)*
```
bash scripts/launch_server_mock.sh
```

## ⚙️ Advanced Configuration
- **Multi-GPU Support:** Modify launch to specify GPU workers.
    - `--parallel-size`: Number of workers
    - `--max-batch-size 1`: Max batch size per worker
- **Mochi Setting:**
    - `--num-frames`: Number of frames
    - `--num-inference-steps`: Number of diffusion steps
    - `--fps`: Output video FPS

## Happy Generating! 🎬✨

*(Documentation last updated: 2025-04-21)*