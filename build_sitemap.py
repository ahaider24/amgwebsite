#!/usr/bin/env python3
"""Regenerate sitemap.xml from the pages that actually exist.

The hand-maintained sitemap carried no lastmod on any URL, which removes the
main signal Google uses to decide what to recrawl, and it grew by appending new
pages to the bottom without a priority. The six URLs Google had never crawled as
of 2026-09-10 were all in that appended block.

lastmod comes from git, because the working tree mtime changes on every checkout
and would tell Google every page changed at once, which is worth nothing.

Pages carrying <meta name="robots" content="noindex"> are excluded, since asking
Google to crawl a page you told it not to index wastes crawl budget on a site
that has very little of it.

Usage: python3 build_sitemap.py [--check]
  --check exits 1 if the file on disk differs from what would be generated.
"""
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = "https://amirgetsjobs.com"

# Priority is a weak hint at best, but an explicit one beats an absent one and
# it documents which pages we actually care about.
PRIORITY = {
    "/": "1.0",
    "/ai-marketing-agency-fresno": "0.9",
    "/ai-agency-los-angeles": "0.9",
    "/ai-seo": "0.9",
    "/ai-agents": "0.9",
    "/home-services-marketing": "0.9",
    "/diagnostic": "0.9",
    "/pricing": "0.9",
    "/results": "0.8",
    "/ai-seo-patriot-crane-results": "0.8",
    "/ai-seo-quality-beverage-results": "0.8",
    "/reviews": "0.8",
    "/roofing-marketing": "0.8",
    "/plumber-marketing": "0.8",
    "/hvac-marketing": "0.8",
    "/contractor-marketing": "0.8",
    "/law-firm-marketing": "0.8",
    "/healthcare-marketing": "0.8",
    "/finance-marketing": "0.8",
    "/b2b-marketing": "0.8",
    "/ai-workflows": "0.8",
    "/paid-ads": "0.8",
    "/web-design-development": "0.8",
    "/content-strategy": "0.7",
    "/about": "0.6",
    "/field-notes": "0.6",
    "/what-ai-can-do": "0.6",
    "/ai-agent-for-home-service-business": "0.6",
    "/seo-geo-playbook": "0.6",
    "/ai-search-shift": "0.5",
    "/privacy": "0.3",
    "/terms": "0.3",
}
DEFAULT_PRIORITY = "0.6"

NOINDEX = re.compile(r'<meta[^>]+name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', re.I)


def git_lastmod(path: Path) -> str:
    """Last commit date touching this file, or today if git has never seen it."""
    try:
        out = subprocess.run(
            ["git", "-C", str(ROOT), "log", "-1", "--format=%cs", "--", path.name],
            capture_output=True, text=True, timeout=20)
        stamp = out.stdout.strip()
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", stamp):
            return stamp
    except Exception:
        pass
    return datetime.now(timezone.utc).date().isoformat()


def slug_for(path: Path) -> str:
    return "/" if path.stem == "index" else "/" + path.stem


def build() -> str:
    entries = []
    for path in sorted(ROOT.glob("*.html")):
        html = path.read_text(errors="ignore")
        if NOINDEX.search(html):
            continue
        slug = slug_for(path)
        entries.append((slug, git_lastmod(path),
                        PRIORITY.get(slug, DEFAULT_PRIORITY)))
    # Highest priority first, then most recently changed. Crawlers do not have
    # to honour order, but it costs nothing and reads correctly.
    entries.sort(key=lambda e: (-float(e[2]), e[0]))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for slug, lastmod, priority in entries:
        loc = BASE + ("/" if slug == "/" else slug)
        lines.append(f"  <url><loc>{loc}</loc><lastmod>{lastmod}</lastmod>"
                     f"<priority>{priority}</priority></url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main() -> int:
    target = ROOT / "sitemap.xml"
    generated = build()
    count = generated.count("<url>")
    if "--check" in sys.argv:
        current = target.read_text() if target.exists() else ""
        if current != generated:
            print(f"sitemap.xml is stale, regenerate it ({count} URLs expected)")
            return 1
        print(f"sitemap.xml is current ({count} URLs)")
        return 0
    target.write_text(generated)
    print(f"wrote {target.relative_to(ROOT)} with {count} URLs, each carrying lastmod")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
