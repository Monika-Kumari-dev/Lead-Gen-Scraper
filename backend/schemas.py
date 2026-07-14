from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class LeadOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # pydantic v1: use `class Config: orm_mode = True` instead

    id: int
    company_name: str
    industry: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    qa_status: Optional[str] = None
    fail_reason: Optional[str] = None
    qa_notes: Optional[str] = None
    scraped_at: Optional[datetime] = None
    image_url: Optional[str] = None