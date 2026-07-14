"""
POST /api/search - kick off a scrape run for chosen industries/regions.

For now this runs synchronously and returns leads directly. Once the
scraper is real (and slow, given rate limiting), swap this for a
background task (FastAPI BackgroundTasks or a task queue) and have the
frontend poll a /status endpoint - that's what the "progress indicator"
in the React dashboard will hook into.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from scraper.maps_scraper import run_maps_scrape
from scraper.directory_scraper import run_directory_scrape
from database import get_db, engine, Base
from models.lead import Lead

# Create the leads table if it doesn't exist yet (safe to call every startup).
Base.metadata.create_all(bind=engine)

router = APIRouter()


class SearchRequest(BaseModel):
    regions: List[str]
    include_maps: bool = True
    include_directories: bool = True


@router.post("/")
def start_search(payload: SearchRequest, db: Session = Depends(get_db)):
    leads = []

    if payload.include_maps:
        leads.extend(run_maps_scrape(regions=payload.regions))

    if payload.include_directories:
        for region in payload.regions:
            leads.extend(run_directory_scrape(region))

    # Save each scraped lead to the database so it's available for
    # /api/results and /api/export/csv afterward.
    saved_leads = []
    for lead_data in leads:
        db_lead = Lead(
            company_name=lead_data.get("company_name") or "Unknown",
            industry=lead_data.get("industry"),
            region=lead_data.get("region"),
            country=lead_data.get("country"),
            website=lead_data.get("website"),
            email=lead_data.get("email"),
            phone=lead_data.get("phone"),
            address=lead_data.get("address"),
            image_url=lead_data.get("image_url"),
            source=lead_data.get("source"),
            source_url=lead_data.get("source_url"),
        )
        db.add(db_lead)
        saved_leads.append(lead_data)

    db.commit()

    return {"count": len(saved_leads), "leads": saved_leads}
