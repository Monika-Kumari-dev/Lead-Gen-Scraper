"""
Simple rate limiter to avoid getting blocked mid-run.

Use before every request/page load:
    from scraper.rate_limiter import RateLimiter
    limiter = RateLimiter()
    ...
    limiter.wait()   # call before each request
"""

import random
import time

from scraper.config import (
    MIN_DELAY_SECONDS,
    MAX_DELAY_SECONDS,
    REQUESTS_BEFORE_COOLDOWN,
    COOLDOWN_SECONDS,
)


class RateLimiter:
    def __init__(self):
        self.request_count = 0

    def wait(self):
        """Call this immediately before each request/page load."""
        self.request_count += 1

        # Longer cooldown every N requests to avoid sustained hammering.
        if self.request_count % REQUESTS_BEFORE_COOLDOWN == 0:
            print(f"[rate_limiter] {self.request_count} requests done - cooling down {COOLDOWN_SECONDS}s")
            time.sleep(COOLDOWN_SECONDS)
        else:
            delay = random.uniform(MIN_DELAY_SECONDS, MAX_DELAY_SECONDS)
            time.sleep(delay)
