MODEL_NAME = "Qwen/Qwen2.5-VL-3B-Instruct"
device = "cuda"  # or "cpu" if no GPU
MAX_NEW_TOKENS = 512

PROMPT_TEMPLATE = """
You are an AI invoice extractor. Extract the following fields from the invoice image attached in the message:

{
  "supplier_name": "Name of the supplier",
  "total_price": 123.45,
  "payment_method": "Cash, Card, or Other",
  "date_time": "YYYY-MM-DD HH:MM",
  "confidence": 0.95
}

Rules:
- Return JSON only, no explanations.
- If a field cannot be found, use empty string "" or null.
- Fill the confidence field with a float (0-1) indicating your confidence in the extraction.
"""