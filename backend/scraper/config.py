"""
Scraper configuration: target industries, regions, and rate-limiting.

Fill in SOURCE_LIST once it's locked with Ashish. Keeping it here (not
hardcoded in the scraper) means adding/changing sources doesn't touch
scraper logic - just this file.
"""

# --- Target scope (per Ashish's email) ---
INDUSTRIES = [
    "pharma_manufacturing",
    "general_manufacturing",
]

REGIONS = [
    "India",
    "Southeast Asia",
    "Middle East",
    "Europe",
]

# --- Google Maps search categories ---
# One entry per (industry, query) - queries run per region.
MAPS_CATEGORIES = [
    "pharmaceutical manufacturer",
    "pharmaceutical company",
    "industrial manufacturer",
    "manufacturing company",
    "chemical manufacturer",
]

# --- Directory sites (fill in once locked) ---
# Example structure - add real category paths as you research each one.
DIRECTORY_SOURCES = {
    "India": [
        {"name": "IndiaMART", "url": "https://dir.indiamart.com/", "category_path": "impcat/pharmaceutical-drug.html"},
        {"name": "TradeIndia", "url": "https://www.tradeindia.com/", "category_path": ""},
        {"name": "ExportersIndia", "url": "https://www.exportersindia.com/", "category_path": ""},
    ],
    "Southeast Asia": [
        {"name": "Kompass Singapore", "url": "https://sg.kompass.com/", "category_path": ""},
        {"name": "Kompass Malaysia", "url": "https://my.kompass.com/", "category_path": ""},
        {"name": "Kompass Thailand", "url": "https://th.kompass.com/", "category_path": ""},
        {"name": "Kompass Vietnam", "url": "https://vn.kompass.com/", "category_path": ""},
        {"name": "Kompass Indonesia", "url": "https://id.kompass.com/", "category_path": ""},
        {"name": "Kompass Philippines", "url": "https://ph.kompass.com/", "category_path": ""},
        {"name": "BiopharmGuy Asia", "url": "https://biopharmguy.com/links/company-by-location-asia.php", "category_path": ""},
    ],
    "Middle East": [
        {"name": "Kompass UAE", "url": "https://ae.kompass.com/", "category_path": ""},
        {"name": "Kompass Saudi Arabia", "url": "https://sa.kompass.com/", "category_path": ""},
        {"name": "BiopharmGuy Middle East", "url": "https://biopharmguy.com/links/company-by-location-middle-east.php", "category_path": ""},
        {"name": "Gulf Business Directory", "url": "https://gulfbusiness.tradeholding.com/", "category_path": ""},
    ],
    "Europe": [
        {"name": "Europages", "url": "https://www.europages.com/", "category_path": "bs/chemicals-pharmaceuticals/pharmaceuticals"},
        {"name": "Kompass Germany", "url": "https://de.kompass.com/", "category_path": ""},
        {"name": "Kompass France", "url": "https://fr.kompass.com/", "category_path": ""},
    ],
}

# --- Rate limiting (per Ashish's note: Google Maps + directories will
# block/rate-limit at volume if hit continuously) ---
MIN_DELAY_SECONDS = 3
MAX_DELAY_SECONDS = 8

# Rotate/limit requests per "session" before pausing longer, to avoid
# hammering the same IP continuously.
REQUESTS_BEFORE_COOLDOWN = 25
COOLDOWN_SECONDS = 60
