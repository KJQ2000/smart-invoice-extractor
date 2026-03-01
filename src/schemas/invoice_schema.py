from pydantic import BaseModel
from typing import Optional

class FieldWithConfidence(BaseModel):
    value: Optional[str]  # or float for numeric fields
    confidence: float = 0.0

class InvoiceResponse(BaseModel):
    supplier_name: FieldWithConfidence
    total_price: FieldWithConfidence
    payment_method: FieldWithConfidence
    date_time: FieldWithConfidence