"""
GET   /api/results/          - paginated, searchable list of saved leads
GET   /api/results/{id}      - single lead detail
PATCH /api/results/{id}/qa   - update QA status/fail_reason/notes
"""
import math
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from pydantic import BaseModel

from database import get_db
from models.lead import Lead
from schemas import LeadOut

router = APIRouter()


@router.get("/")
def list_leads(
    page: int = 1,
    limit: int = 12,
    search: Optional[str] = None,
    region: Optional[str] = None,
    industry: Optional[str] = None,
    qa_status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Lead)

    if search:
        like = f"%{search}%"
        query = query.filter(or_(Lead.company_name.ilike(like), Lead.address.ilike(like)))
    if region:
        query = query.filter(Lead.region == region)
    if industry:
        query = query.filter(Lead.industry == industry)
    if qa_status:
        query = query.filter(Lead.qa_status == qa_status)

    total = query.count()
    total_pages = max(math.ceil(total / limit), 1)
    page = max(page, 1)

    leads = (
        query.order_by(Lead.scraped_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "data": [LeadOut.model_validate(l) for l in leads],
        "pagination": {"page": page, "limit": limit, "total": total, "totalPages": total_pages},
    }


@router.get("/{lead_id}", response_model=LeadOut)
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


class QaUpdate(BaseModel):
    qa_status: str
    fail_reason: Optional[str] = None
    qa_notes: Optional[str] = None


@router.patch("/{lead_id}/qa", response_model=LeadOut)
def update_qa(lead_id: int, payload: QaUpdate, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    lead.qa_status = payload.qa_status
    lead.fail_reason = payload.fail_reason
    lead.qa_notes = payload.qa_notes
    db.commit()
    db.refresh(lead)
    return lead