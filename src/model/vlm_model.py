from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration
import torch
from src.constants import MODEL_NAME, device

print("Loading model...")

processor = AutoProcessor.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    MODEL_NAME, trust_remote_code=True, torch_dtype=torch.float16,  # use float16 to save GPU memory
).to(device)
model.eval()

print("Model loaded successfully!")