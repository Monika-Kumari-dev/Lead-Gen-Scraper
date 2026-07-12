"""
Selenium scraper for Google Maps listings.

Maps needs a real browser session (JS-rendered, infinite-scroll results),
which is why this uses Selenium instead of BeautifulSoup - unlike the
directory sites, which are static HTML (see directory_scraper.py).

Selectors below were built from real inspected HTML (right-click -> Inspect
on a live Maps search) - not guessed. Google's class names are short,
auto-generated strings that can change over time; if this breaks later,
re-inspect a live search the same way and update the selectors here.
"""

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scraper.rate_limiter import RateLimiter
from scraper.config import MAPS_CATEGORIES, REGIONS

FEED_SELECTOR = "div[role='feed']"
CARD_SELECTOR = "div[role='article']"
MAX_SCROLLS = 8  # bounds how many times we scroll for more results per search


def build_driver(headless: bool = True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1280,900")

    # Selenium 4.6+ has built-in driver management (Selenium Manager) -
    # it downloads and matches the right ChromeDriver automatically.
    return webdriver.Chrome(options=options)


def _parse_card(card):
    """Extract lead fields from one result card element."""
    lead = {
        "company_name": None,
        "website": None,
        "phone": None,
        "address": None,
        "source": "google_maps",
    }

    try:
        name_link = card.find_element(By.CSS_SELECTOR, "a.hfpxzc")
        lead["company_name"] = name_link.get_attribute("aria-label")
        lead["source_url"] = name_link.get_attribute("href")
    except Exception:
        pass

    try:
        website_link = card.find_element(By.CSS_SELECTOR, "a[aria-label^='Visit']")
        lead["website"] = website_link.get_attribute("href")
    except Exception:
        pass

    try:
        info_blocks = card.find_elements(By.CSS_SELECTOR, "div.W4Efsd")
        if info_blocks:
            text = info_blocks[0].text
            parts = [p.strip() for p in text.split("\xb7")]
            if len(parts) > 1:
                lead["address"] = parts[-1]
    except Exception:
        pass

    try:
        phone_span = card.find_element(By.CSS_SELECTOR, "span.UsdlK")
        lead["phone"] = phone_span.text
    except Exception:
        pass

    return lead


def search_maps(query: str, region: str, limiter: RateLimiter, driver=None):
    """
    Search Google Maps for `query` in `region` and return a list of
    raw lead dicts.
    """
    owns_driver = driver is None
    if owns_driver:
        driver = build_driver()

    results = []
    try:
        limiter.wait()
        search_query = f"{query} {region}"
        driver.get(f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}")

        wait = WebDriverWait(driver, 15)
        feed = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, FEED_SELECTOR)))

        seen_count = 0
        for _ in range(MAX_SCROLLS):
            driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight", feed
            )
            time.sleep(2)
            cards_now = len(feed.find_elements(By.CSS_SELECTOR, CARD_SELECTOR))
            if cards_now == seen_count:
                break
            seen_count = cards_now

        # Cards are already loaded in the DOM at this point - reading their
        # text/attributes is local parsing, not a new network request, so
        # no rate-limit delay is needed here (unlike page loads above).
        cards = feed.find_elements(By.CSS_SELECTOR, CARD_SELECTOR)
        for card in cards:
            lead = _parse_card(card)
            if lead["company_name"]:
                lead["region"] = region
                results.append(lead)

    finally:
        if owns_driver:
            driver.quit()

    return results


def run_maps_scrape(industries=None, regions=None):
    """Loop over categories x regions and collect all leads."""
    regions = regions or REGIONS
    limiter = RateLimiter()
    driver = build_driver()

    all_leads = []
    try:
        for region in regions:
            for query in MAPS_CATEGORIES:
                try:
                    leads = search_maps(query, region, limiter, driver=driver)
                    all_leads.extend(leads)
                except Exception as e:
                    print(f"[maps_scraper] Skipped '{query}' in {region}: {e}")
                    continue
    finally:
        driver.quit()

    return all_leads
