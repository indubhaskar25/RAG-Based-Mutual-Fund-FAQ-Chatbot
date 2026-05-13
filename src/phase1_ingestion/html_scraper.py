"""
Phase 1: HTML Scraper
Extracts clean text from Groww.in mutual fund pages.
Handles scheme pages, educational pages, and category pages.
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HTMLScraper:
    """Scrapes clean text from Groww HTML pages."""

    def __init__(self, user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"):
        self.headers = {"User-Agent": user_agent}
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _normalize_text(self, text: str) -> str:
        """
        Performs Unicode normalization and removes redundant whitespace/boilerplate noise.
        """
        import unicodedata
        import re

        # Unicode Normalization (NFKC)
        text = unicodedata.normalize("NFKC", text)

        # Remove redundant whitespace within lines
        text = re.sub(r"[ \t]+", " ", text)

        # Split into lines and filter out empty or boilerplate-heavy lines
        boilerplate_keywords = [
            "demat account", "login", "register", "open demat", "track returns",
            "intraday", "mtfs", "stock events", "pricing", "blog", "careers",
            "invest in stocks", "invest in mutual funds", "share market today"
        ]
        
        lines = []
        for line in text.split("\n"):
            line = line.strip()
            if not line:
                continue
            
            # Skip lines that are just boilerplate keywords (case-insensitive)
            if line.lower() in boilerplate_keywords:
                continue
                
            lines.append(line)

        # Reconstruct with consistent single newlines
        return "\n".join(lines)

    def scrape(self, url: str) -> Optional[str]:
        """
        Fetches the URL and extracts clean text without boilerplate.
        """
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Remove scripts, styles, and common boilerplate navigation tags
            for element in soup(["script", "style", "header", "footer", "nav", "aside", "noscript", "button"]):
                element.extract()

            # Extract text with separator
            text = soup.get_text(separator="\n", strip=True)

            # Apply normalization
            clean_text = self._normalize_text(text)

            if len(clean_text) < 50:
                logger.warning(f"Very little text extracted from {url} ({len(clean_text)} chars)")
                return None

            logger.info(f"Successfully scraped and normalized {url} — {len(clean_text)} characters")
            return clean_text

        except requests.exceptions.Timeout:
            logger.error(f"Timeout scraping {url}")
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error scraping {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {e}")
            return None
