"""
BeautifulSoup scraper for static directory pages (IndiaMART, Europages, etc.)
"""

import requests
from bs4 import BeautifulSoup

from scraper.rate_limiter import RateLimiter
from scraper.config import DIRECTORY_SOURCES

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def parse_indiamart_page(html: str, source_url: str):
    """
    Parse an IndiaMART category listing page.
    Each listing card is <li class="pCard1">.
    """
    soup = BeautifulSoup(html, "html.parser")
    leads = []

    for card in soup.select("li.pCard1"):
        name_link = card.select_one(".wlc1 a")
        if not name_link:
            continue

        company_name = name_link.get_text(strip=True)
        website = name_link.get("href")

        locality_tag = card.select_one("[itemprop='addressLocality']")
        address = locality_tag.get_text(strip=True) if locality_tag else None

        leads.append({
            "company_name": company_name,
            "website": website,
            "email": None,
            "phone": None,
            "address": address,
            "source": "directory",
            "source_url": source_url,
        })

    return leads


def parse_tradeindia_page(html: str, source_url: str):
    """
    Parse a TradeIndia category listing page.

    Each card is <div class="product-info-cnt responsive-card">. Company
    name + TradeIndia profile link are in .supplier-details .top-cont h3 a.
    City is the second <h3> in that same block. Note: the link goes to the
    company's TradeIndia profile page, not their own external website
    (unlike IndiaMART) - still a valid contact path.
    """
    soup = BeautifulSoup(html, "html.parser")
    leads = []

    for card in soup.select("div.product-info-cnt"):
        top_cont = card.select_one(".supplier-details .top-cont")
        if not top_cont:
            continue

        name_link = top_cont.select_one("h3 a.company-url")
        if not name_link:
            continue

        company_name = name_link.get_text(strip=True)
        profile_url = name_link.get("href")

        headings = top_cont.select("h3")
        address = headings[1].get_text(strip=True) if len(headings) > 1 else None

        leads.append({
            "company_name": company_name,
            "website": profile_url,  # TradeIndia profile page, not external site
            "email": None,
            "phone": None,
            "address": address,
            "source": "directory",
            "source_url": source_url,
        })

    return leads


def parse_exportersindia_page(html: str, source_url: str):
    """
    Parse an ExportersIndia category listing page.

    Each card is <div class="l3Inn ...">. Company name + profile link are
    in .com_address .com_addOth h3._company a.com_nam. Location is in
    .com_address ._address span._fAdre. Link goes to the company's
    ExportersIndia profile page, not their external website.
    """
    soup = BeautifulSoup(html, "html.parser")
    leads = []

    for card in soup.select("div.l3Inn"):
        name_link = card.select_one(".com_addOth h3._company a.com_nam")
        if not name_link:
            continue

        company_name = name_link.get_text(strip=True)
        profile_url = name_link.get("href")

        address_span = card.select_one("._address span._fAdre")
        address = address_span.get_text(strip=True) if address_span else None

        leads.append({
            "company_name": company_name,
            "website": profile_url,  # ExportersIndia profile page, not external site
            "email": None,
            "phone": None,
            "address": address,
            "source": "directory",
            "source_url": source_url,
        })

    return leads


PARSERS = {
    "IndiaMART": parse_indiamart_page,
    "TradeIndia": parse_tradeindia_page,
    "ExportersIndia": parse_exportersindia_page,
}


def scrape_directory_page(url: str, source_name: str, limiter: RateLimiter):
    """Fetch a directory page and parse it with the right parser for that site."""
    limiter.wait()
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()

    parser = PARSERS.get(source_name)
    if parser is None:
        return []

    return parser(response.text, url)


def run_directory_scrape(region: str):
    """
    Loop over configured directory sources for a region.

    Each source is wrapped in try/except so one site failing (blocked,
    down, wrong URL, etc.) does not crash the whole search - we log
    the failure reason and move on to the next source.
    """
    limiter = RateLimiter()
    sources = DIRECTORY_SOURCES.get(region, [])

    all_leads = []
    for source in sources:
        listing_url = source["url"] + source.get("category_path", "")
        try:
            leads = scrape_directory_page(listing_url, source["name"], limiter)
            for lead in leads:
                lead["region"] = region
            all_leads.extend(leads)
        except Exception as e:
            print(f"[directory_scraper] Skipped {source['name']} ({listing_url}): {e}")
            continue

    return all_leads
