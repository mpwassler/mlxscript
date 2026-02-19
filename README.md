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

## License

MIT
