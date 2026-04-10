# backend/models.py
from pydantic import BaseModel
from typing import List, Optional

class ScrapeItem(BaseModel):
    title: str
    source: str
    category: str
    price: Optional[str] = None
    date: str