import json
import sys
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from mlx_vlm import load, generate
from mlx_vlm.prompt_utils import apply_chat_template
from mlx_vlm.utils import load_config
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
MODEL_PATH = os.getenv("MODEL_PATH", "mlx-community/Qwen2.5-VL-7B-Instruct-4bit")
PORT = int(os.getenv("PORT", "8080"))

print(f"⬇️  Loading {MODEL_PATH}...")

try:
    # Load with 4-bit quantization to keep memory usage around 6GB
    model, processor = load(MODEL_PATH, trust_remote_code=True)
    config = load_config(MODEL_PATH, trust_remote_code=True)
except Exception as e:
    print(f"❌ Error loading 7B model. Ensure you have ~6GB of free RAM: {e}")
    sys.exit(1)

print(f"✅ 7B Model Loaded. Server listening on port {PORT}...")

class LocalLlmHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data)
            # PROMPT TIP: The 7B model can handle much more complex system instructions.
            prompt_text = data.get("prompt", "")
            image_path = data.get("image", None)
            
            if not image_path:
                self.send_error(400, "Missing 'image' path.")
                return

            # Format for Qwen
            formatted_prompt = apply_chat_template(
                processor, 
                config, 
                prompt_text, 
                num_images=1
            )

            # Generate with optimized 16GB settings
            output = generate(
                model, 
                processor, 
                formatted_prompt, 
                [image_path], 
                verbose=True,
                temp=0.2,
                max_tokens=700, # 7B can handle longer, more detailed responses
                repetition_penalty=1.4, # Critical for avoiding the loops you saw earlier
                max_pixels=1004544  # Keeps vision processing fast on M1
            )
            
            response = {"response": output.text}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

        except Exception as e:
            self.send_error(500, f"Server Error: {str(e)}")

def run():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, LocalLlmHandler)
    print(f"🚀 Server Running. M1 GPU is active.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    run()