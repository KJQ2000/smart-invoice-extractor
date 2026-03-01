Smart Invoice Extractor is a web application that uses Qwen2.5-VL, a multimodal AI model, to automatically extract key information from invoice images. The app is built with FastAPI for the backend and a simple HTML/JS frontend with a progress bar for user feedback.

Features
Upload invoice images through a web interface.

Extract fields automatically:
Supplier name
Total price
Payment method
Date and time
Confidence score
Display results in a table.
Progress bar during extraction.
JSON output for integration.

Requirements
Python 3.10+
GPU recommended (CUDA enabled) for faster inference
Python packages:
transformers
torch
Pillow
fastapi
uvicorn
jinja2

Installation
Clone the repository:
git clone https://github.com/KJQ2000/smart-invoice-extractor.git
cd smart_invoice

Create a virtual environment:
python -m venv vlm_env

Activate the environment:
Windows:
vlm_env\Scripts\activate

Linux/macOS:
source vlm_env/bin/activate

Install dependencies:
pip install -r requirements.txt

Tip: Create a requirements.txt with the following packages:
fastapi
uvicorn
transformers
torch
Pillow
jinja2
tqdm

Place your model files (GGUF or Hugging Face) inside the models/ folder.
Usage
Start the FastAPI server:
uvicorn main:app --reload
Open your browser and navigate to:
http://127.0.0.1:8000
Upload an invoice image and click Extract.The extracted data will appear in the table below the upload, and the progress bar will disappear once extraction is complete.

Logging
The backend logs important steps, such as image loading, model input preparation, and raw AI output.
Errors in JSON parsing or extraction are logged for easier debugging.

Notes
Large model files are ignored by Git (.gitignore) and must be manually placed in models/.
GPU is recommended; otherwise, inference may be slow.
The AI uses a prompt-based extraction strategy to output JSON directly.

License
This project is for personal or internal use.
