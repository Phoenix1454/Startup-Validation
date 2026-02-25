"""Firecrawl-based domain validation tool."""

import os
from typing import Optional

from firecrawl import FirecrawlApp


def validate_domain(domain: str) -> dict:
    """Check whether a domain is live using Firecrawl.

    Args:
        domain: The bare domain name to validate, e.g. ``techvision.com``.

    Returns:
        A dict with keys:
          - ``domain``         – the input domain
          - ``exists``         – True if the domain is reachable and has content
          - ``content_preview``– first 500 characters of the scraped markdown (if any)
          - ``status``         – human-readable status string
    """
    api_key: Optional[str] = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        raise EnvironmentError("FIRECRAWL_API_KEY environment variable is not set.")

    app = FirecrawlApp(api_key=api_key)
    url = f"https://{domain}"

    try:
        result = app.scrape_url(url, formats=["markdown"])

        # firecrawl-py ≥1.0 returns a ScrapeResponse object; earlier versions a dict.
        if hasattr(result, "markdown"):
            markdown = result.markdown or ""
            success = result.success if hasattr(result, "success") else bool(markdown)
        else:
            markdown = result.get("markdown", "") or ""
            success = result.get("success", bool(markdown))

        if success and markdown:
            return {
                "domain": domain,
                "exists": True,
                "content_preview": markdown[:500],
                "status": "active",
            }
        else:
            return {
                "domain": domain,
                "exists": False,
                "content_preview": "",
                "status": "unreachable",
            }

    except Exception as exc:  # noqa: BLE001
        return {
            "domain": domain,
            "exists": False,
            "content_preview": "",
            "status": f"error: {exc}",
        }
