"""
GET /api/results - fetch stored leads for the dashboard's results table.
PATCH /api/results/{id}/qa - log a spot-check pass/fail + reason for a lead.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from database import get_db
from models.lead import Lead

router = APIRouter()


class LeadOut(BaseModel):
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

    class Config:
        from_attributes = True


class QAUpdate(BaseModel):
    qa_status: str  # "pass" or "fail"
    fail_reason: Optional[str] = None


@router.get("/", response_model=list[LeadOut])
def get_results(
    region: Optional[str] = None,
    industry: Optional[str] = None,
    qa_status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Lead)

    if region:
        query = query.filter(Lead.region == region)
    if industry:
        query = query.filter(Lead.industry == industry)
    if qa_status:
        query = query.filter(Lead.qa_status == qa_status)

    return query.order_by(Lead.id.desc()).all()


@router.patch("/{lead_id}/qa", response_model=LeadOut)
def update_qa(lead_id: int, payload: QAUpdate, db: Session = Depends(get_db)):
    """Used by the manual spot-check step to log pass/fail + reason why."""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Lead not found")

    lead.qa_status = payload.qa_status
    lead.fail_reason = payload.fail_reason
    db.commit()
    db.refresh(lead)
    return lead
