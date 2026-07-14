"""
GET /api/export/csv - export leads as a downloadable CSV using pandas.
"""

import io
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import pandas as pd

from database import get_db
from models.lead import Lead

router = APIRouter()


@router.get("/csv")
def export_csv(db: Session = Depends(get_db)):
    leads = db.query(Lead).all()

    rows = [
        {
            "company_name": l.company_name,
            "industry": l.industry,
            "region": l.region,
            "country": l.country,
            "website": l.website,
            "email": l.email,
            "phone": l.phone,
            "address": l.address,
            "source": l.source,
            "qa_status": l.qa_status,
            "fail_reason": l.fail_reason,
        }
        for l in leads
    ]

    df = pd.DataFrame(rows)
    stream = io.StringIO()
    df.to_csv(stream, index=False)

    return StreamingResponse(
        iter([stream.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=leads_export.csv"},
    )
