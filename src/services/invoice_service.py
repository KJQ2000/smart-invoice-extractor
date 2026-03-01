# src/services/invoice_service.py
import logging
from PIL import Image
import json, re
import torch
from src.model.vlm_model import model, processor
from src.constants import PROMPT_TEMPLATE, MAX_NEW_TOKENS

# -----------------------------
# Logging setup
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

def extract_invoice_fields(image_path: str):
    try:
        logger.info(f"Loading image: {image_path}")
        image = Image.open(image_path).convert("RGB")
        logger.info(f"Image loaded successfully. Size: {image.size}")

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": PROMPT_TEMPLATE},
                ],
            }
        ]

        logger.info("Applying chat template...")
        chat_prompt = processor.apply_chat_template(
            messages,
            tokenize=False,  # important: False for image-text inputs
            add_generation_prompt=True
        )

        logger.info("Preparing model inputs...")
        inputs = processor(
            text=chat_prompt,
            images=[image],
            return_tensors="pt"
        ).to(model.device)
        logger.info("Inputs prepared successfully.")

        logger.info("Generating model output...")
        outputs = model.generate(**inputs, max_new_tokens=MAX_NEW_TOKENS)
        raw_text = processor.decode(outputs[0], skip_special_tokens=True)
        logger.info(f"Raw model output:\n{raw_text}")

        # -----------------------------
        # Extract JSON robustly
        # -----------------------------
        logger.info("Extracting JSON from raw output...")

        # 1️⃣ Try JSON inside ```json ... ``` first
        code_json_match = re.search(r"```json\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
        if code_json_match:
            json_str = code_json_match.group(1)
        else:
            # 2️⃣ fallback: any {...} in the output
            any_json_match = re.search(r"\{.*?\}", raw_text, re.DOTALL)
            json_str = any_json_match.group(0) if any_json_match else None

        if json_str:
            try:
                data = json.loads(json_str)
                logger.info("JSON extracted successfully.")
                return {
                    "supplier_name": data.get("supplier_name", ""),
                    "total_price": data.get("total_price"),
                    "payment_method": data.get("payment_method", ""),
                    "date_time": data.get("date_time", ""),
                    "confidence": data.get("confidence", None)
                }
            except Exception as e:
                logger.error(f"JSON parsing failed: {e}")
                return {"error": f"JSON parsing failed: {e}", "raw_output": raw_text}

        logger.error("No JSON detected in model output.")
        return {"error": "No JSON detected", "raw_output": raw_text}

    except Exception as e:
        logger.exception("Exception during extraction:")
        return {"error": str(e)}