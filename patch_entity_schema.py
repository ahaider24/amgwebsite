#!/usr/bin/env python3
"""Declare the corroboration AMG has already earned.

The schema was well built and had one hole: the organisation's sameAs listed a
single URL. Everything else the brand has earned, the Fresno Chamber listing,
the Business Journal archive, Instagram, GitHub, was real but never claimed, so
nothing told a search engine those pages are the same entity as this site.

The second hole is the name. This site writes "AmirGetsJobs" 172 times. Fast
Company, Fast Company Brasil, Marketer Magazine and Yelp all write "Amir Gets
Jobs". Without alternateName those are two entities, and the strongest link in
the profile, a DR 92 Fast Company placement, is anchored to the half the site
never claims.

Every URL here was fetched and confirmed to exist on 2026-09-10. The ones that
answer 403 or 405 to a HEAD request (Yelp, LinkedIn, Business Journal) are bot
blocks on pages already read in a browser, not missing pages.

Usage: python3 patch_entity_schema.py [--check]
"""
import glob
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

ALTERNATE_NAMES = ["Amir Gets Jobs", "AMG"]

ORG_SAMEAS = [
    "https://www.yelp.com/biz/amir-gets-jobs-fresno",
    "https://business.fresnochamber.com/list/member/amirgetsjobs-32761",
    "https://www.instagram.com/amirgetsjobs",
    "https://github.com/AmirGetsJobs",
    "https://thebusinessjournal.com/tag/amirgetsjobs/",
]

PERSON_SAMEAS = [
    "https://www.linkedin.com/in/amhaider",
    ("https://www.fastcompany.com/91530813/"
     "11-ways-to-signal-ai-fluency-on-your-resume-resumes-ai-fluenc"),
    ("https://fastcompanybrasil.com/worklife/"
     "11-formas-de-mostrar-no-curriculo-que-voce-sabe-usar-ia-e-se-destacar-no-mercado/"),
    "https://thebusinessjournal.com/fresno-ai-agency-chatbot-referrals-amir-haider/",
]

BLOCK = re.compile(
    r'(<script[^>]*application/ld\+json[^>]*>)(.*?)(</script>)', re.S)


def patch_nodes(data) -> bool:
    """Walk the graph and top up the two entity nodes. True if anything moved."""
    changed = False
    nodes = data.get("@graph") if isinstance(data, dict) else None
    if nodes is None:
        nodes = data if isinstance(data, list) else [data]
    for node in nodes:
        if not isinstance(node, dict):
            continue
        node_id = node.get("@id", "")
        if node_id.endswith("#business"):
            if node.get("alternateName") != ALTERNATE_NAMES:
                node["alternateName"] = ALTERNATE_NAMES
                changed = True
            # Union, never replace: a page may legitimately carry extras.
            merged = list(dict.fromkeys(
                (node.get("sameAs") or []) + ORG_SAMEAS))
            if merged != node.get("sameAs"):
                node["sameAs"] = merged
                changed = True
        elif node_id.endswith("#founder"):
            merged = list(dict.fromkeys(
                (node.get("sameAs") or []) + PERSON_SAMEAS))
            if merged != node.get("sameAs"):
                node["sameAs"] = merged
                changed = True
    return changed


def patch_file(path: Path, check: bool) -> bool:
    html = path.read_text()
    out, touched = [], False
    last = 0
    for m in BLOCK.finditer(html):
        raw = m.group(2).strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue  # leave anything unparseable exactly as it is
        if not patch_nodes(data):
            continue
        rendered = json.dumps(data, indent=1, ensure_ascii=False)
        out.append(html[last:m.start(2)])
        out.append("\n" + rendered + "\n")
        last = m.end(2)
        touched = True
    if not touched:
        return False
    out.append(html[last:])
    if not check:
        path.write_text("".join(out))
    return True


def main() -> int:
    check = "--check" in sys.argv
    hit = [p for p in sorted(ROOT.glob("*.html"))
           if patch_file(p, check)]
    if check:
        if hit:
            print(f"{len(hit)} page(s) have stale entity schema: "
                  + ", ".join(p.name for p in hit))
            return 1
        print("entity schema is current on every page")
        return 0
    print(f"patched {len(hit)} page(s):")
    for p in hit:
        print("  ", p.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
