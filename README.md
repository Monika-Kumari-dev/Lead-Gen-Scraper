# Lead Generation Scraper

Web scraping tool to build a lead list of pharma + general manufacturing
companies across India, Southeast Asia, the Middle East, and Europe.
Sources: Google Maps (Selenium) and static B2B directories (BeautifulSoup).

## Project structure

```
lead-gen-scraper/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── database.py              # SQLAlchemy setup (SQLite dev / MySQL prod)
│   ├── requirements.txt
│   ├── models/
│   │   └── lead.py              # Lead table schema
│   ├── routes/
│   │   ├── search.py            # POST /api/search - trigger scrape
│   │   ├── results.py           # GET /api/results - list/filter leads, QA update
│   │   └── export.py            # GET /api/export/csv - CSV export
│   └── scraper/
│       ├── config.py            # source list, industries, regions, rate limits
│       ├── rate_limiter.py      # delay/cooldown logic
│       ├── maps_scraper.py      # Selenium - Google Maps
│       └── directory_scraper.py # BeautifulSoup - directory sites
└── frontend/                    # React dashboard (set up separately, see below)
```

## Backend setup (Mac)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

You'll also need Google Chrome installed (regular desktop Chrome is fine).
`webdriver-manager` (in requirements.txt) automatically downloads the
matching ChromeDriver the first time `maps_scraper.py` runs - no manual
driver setup needed.

API docs (Swagger UI): http://127.0.0.1:8000/docs

## Frontend setup

Not scaffolded yet - create it with:

```bash
npx create-react-app frontend
cd frontend
npm install axios react-router-dom
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

Dashboard pages to build (per project plan):
- Search form (region/industry filters, triggers POST /api/search)
- Progress indicator (poll a status endpoint while scrape runs)
- Results table (GET /api/results, filterable)
- Export button (hits GET /api/export/csv)
- Settings page (rate-limit values, source list toggles)

