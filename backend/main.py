from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from routes import search, results, export, auth
from auth import get_current_user

app = FastAPI(
    title="Lead Generation Scraper API",
    description="API for scraping and managing manufacturing leads (pharma + general manufacturing).",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(search.router, prefix="/api/search", tags=["search"], dependencies=[Depends(get_current_user)])
app.include_router(results.router, prefix="/api/results", tags=["results"], dependencies=[Depends(get_current_user)])
app.include_router(export.router, prefix="/api/export", tags=["export"], dependencies=[Depends(get_current_user)])


@app.get("/")
def root():
    return {"status": "ok", "message": "Lead Gen Scraper API is running"}