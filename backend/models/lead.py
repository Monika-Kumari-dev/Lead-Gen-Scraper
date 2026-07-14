"""
Lead model - one row per scraped company/lead.

`fail_reason` implements Ashish's spot-check feedback: instead of a plain
pass/fail flag, log WHY a record failed QA (bad_email, dead_site, wrong_industry,
etc.) so patterns can be traced back to specific scraper fixes.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func

from database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)

    company_name = Column(String(255), nullable=False)
    industry = Column(String(100))          # e.g. "pharma_manufacturing", "general_manufacturing"
    region = Column(String(100))            # e.g. "India", "Southeast Asia", "Middle East", "Europe"
    country = Column(String(100))
    image_url = Column(String(500), nullable=True)
    website = Column(String(500))
    email = Column(String(255))
    phone = Column(String(50))
    address = Column(Text)

    source = Column(String(50))             # "google_maps" or "directory"
    source_url = Column(String(500))        # exact search/listing URL the lead came from

    # --- QA / spot-check fields ---
    qa_status = Column(String(20), default="unchecked")   # unchecked | pass | fail
    fail_reason = Column(String(100), nullable=True)       # bad_email_format | dead_site | wrong_industry | duplicate | other
    qa_notes = Column(Text, nullable=True)

    scraped_at = Column(DateTime(timezone=True), server_default=func.now())
