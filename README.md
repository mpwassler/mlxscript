# MLX VLM Server

A simple HTTP server for running Vision Language Models (VLM) on Apple Silicon using [MLX](https://github.com/ml-explore/mlx).

## Features

- Optimized for Apple Silicon (M1/M2/M3).
- Uses `mlx-vlm` for efficient inference.
- Configurable via environment variables.
- Simple JSON API.

## Prerequisites

- macOS with Apple Silicon.
- Python 3.9 or higher.

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd mlxserver
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   Copy the example environment file and adjust as needed:
   ```bash
   cp .env.example .env
   ```

## Usage

1. **Start the server:**
   ```bash
   python run_server.py
   ```

2. **Send a request:**
   The server accepts POST requests at the root endpoint with a JSON body containing a `prompt` and an `image` path.

   Example using `curl`:
   ```bash
   curl -X POST http://localhost:8080 
     -H "Content-Type: application/json" 
     -d '{
       "prompt": "What is in this image?",
       "image": "/path/to/your/image.jpg"
     }'
   ```

## Configuration

You can customize the following in your `.env` file:

- `MODEL_PATH`: The Hugging Face repo ID or local path to the MLX-converted model.
- `PORT`: The port the server will listen on (default: 8080).

## Recommended Models

The MLX Community hosts several optimized models for various use cases. You can change your model by updating the `MODEL_PATH` in your `.env` file.

| Model ID | Best For... | RAM (Approx) |
| :--- | :--- | :--- |
| `mlx-community/Qwen2-VL-72B-Instruct-4bit` | **Ultimate Performance.** Highest accuracy available for MLX. | ~42GB+ |
| `mlx-community/Pixtral-12B-4bit` | **Strong 12B Alternative.** Great for complex visual reasoning. | ~10GB |
| `mlx-community/Qwen2.5-VL-7B-Instruct-4bit` | **State-of-the-Art Accuracy.** Best for complex reasoning and detail. | ~6.5GB |
| `mlx-community/llava-v1.6-mistral-7b-4bit` | **Robust Baseline.** Good balance of speed and reliability. | ~6.0GB |
| `mlx-community/paligemma-3b-mix-448-4bit` | **Speed & Edge Devices.** Faster inference with lower memory footprint. | ~3.5GB |
| `mlx-community/Phi-3-vision-128k-instruct-4bit` | **Document Analysis.** Excellent for OCR and structured data extraction. | ~4.0GB |

### When to use which model?
- **High-RAM Users (32GB/64GB+):** If you have an M1/M2/M3 Max or Ultra, use `Qwen2-VL-72B`. It rivals the best proprietary models (like GPT-4V) in vision reasoning but requires significant Unified Memory.
- **Mid-Range Power (16GB+):** `Pixtral-12B` or `Qwen2.5-VL-7B` are excellent choices. They provide a noticeable jump in "intelligence" over 3B models while remaining very snappy.
- **Detailed Image Analysis:** Use `Qwen2.5-VL-7B`. It has superior vision-language alignment and handles complex reasoning well.
- **Reading Text or Documents (OCR):** `Phi-3-vision` is specifically tuned for high-resolution document processing and extracting structured data.
- **Fast/Real-time Applications:** `PaliGemma-3B` is significantly lighter and offers much lower latency, making it ideal for responsiveness.
- **General Purpose VQA:** `LLaVA-v1.6-Mistral` is a reliable, widely-tested choice for standard vision-question-answering tasks.

### Security Note: `trust_remote_code`
By default, this server uses `trust_remote_code=True`.
- **Why it's needed:** Cutting-edge models like Qwen2.5-VL often have unique architectures or pre-processing logic not yet natively integrated into the `mlx-vlm` library.
- **Risk:** This allows the model repository to execute arbitrary Python code on your machine.
- **Recommendation:** **Only use models from trusted authors** (e.g., `mlx-community`, `google`, `microsoft`, or `Qwen`).

## License

MIT
