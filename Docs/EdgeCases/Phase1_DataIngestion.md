# Edge Cases: Phase 1 - Data Ingestion

This document outlines the edge cases and potential failure modes during the Data Ingestion phase of the Mutual Fund FAQ Chatbot.

## 1. Web Scraper Edge Cases
*   **Dynamic Content / SPA (Single Page Applications):** 
    *   *Issue:* If a mutual fund AMC uses React/Angular where content is loaded via JavaScript, the `requests` library will only retrieve the bare HTML shell, missing the actual text.
    *   *Mitigation:* The architecture currently uses static parsing (`BeautifulSoup`). If dynamic pages are encountered, we would need to upgrade to `Playwright` or `Selenium` to execute JS before parsing.
*   **Anti-Bot Protection:** 
    *   *Issue:* AMC websites may block repeated scraping attempts via Cloudflare or similar WAFs (Web Application Firewalls).
    *   *Mitigation:* Implement rate limiting, randomized user agents, and IP rotation.
*   **Malformed HTML / Unexpected Layout Changes:**
    *   *Issue:* The structure of the AMC site changes, breaking the CSS selectors or tags we rely on to extract clean text.
    *   *Mitigation:* Ensure robust error handling (e.g., fallback to raw text extraction) and regularly monitor logs for scraping failures.

## 2. PDF Parser Edge Cases
*   **Scanned PDFs (Image-based Factsheets):**
    *   *Issue:* Some legacy SIDs or factsheets might be scanned images rather than digital text. `PyMuPDF` will return empty strings.
    *   *Mitigation:* Integrate an OCR pipeline (like `Tesseract` or AWS Textract) as a fallback when text extraction yields < 100 characters.
*   **Multi-Page Tables:**
    *   *Issue:* Mutual fund expense ratio tables or portfolio holdings often span multiple pages. `pdfplumber` might extract these as disjointed tables, losing column headers for the subsequent pages.
    *   *Mitigation:* Implement table merging logic by detecting identical column structures across consecutive pages.
*   **Complex or Nested Tables:**
    *   *Issue:* Cells spanning multiple rows or columns can corrupt the tabular layout during extraction.
    *   *Mitigation:* Post-process the extracted data and convert it safely to Markdown before chunking.
*   **Missing Metadata:**
    *   *Issue:* Documents might lack clear titles or update dates.
    *   *Mitigation:* Mandate manual injection of critical metadata (e.g., `source_url` and `date`) at the time of running the ingestion script to ensure citation integrity.
