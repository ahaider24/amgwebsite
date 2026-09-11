#!/usr/bin/env python3
"""Stop claiming Phoenix as a current market. It is coming soon, not served.

The site already says so in its own navigation: 26 pages carry a nav item
reading "Phoenix / Coming soon". The footer on those same pages says "Serving
Fresno, Los Angeles & Phoenix", and the structured data lists Phoenix as an
areaServed City. So the site states two different facts about the same thing,
which is exactly the ambiguity the entity work is meant to remove.

Two classes of change, both factual, neither a rewrite of Amir's voice:
  1. Structured data: Phoenix City nodes and the plain "Phoenix" string come
     out of areaServed; California goes in as a State, since that is the actual
     coverage.
  2. The repeated "Serving Fresno, Los Angeles & Phoenix" contact line becomes
     "Serving Fresno, Los Angeles & California".

Deliberately NOT touched, because they are prose and belong to Amir:
  - The home page sentence "AmirGetsJobs is an AI marketing agency in Fresno,
    Los Angeles, and Phoenix."
  - The about and field-notes bios.
  - The line "the same systems run for businesses in Los Angeles and Phoenix."
  - The competitor criticism naming "Phoenix Business Owner", which is about
    someone else's template, not a service-area claim.
  - Scroll-world design props using a Phoenix handle.

Usage: python3 fix_service_area.py [--check]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

CALIFORNIA = {"@type": "State", "name": "California"}

CONTACT_LINE = [
    ("Serving Fresno, Los Angeles &amp; Phoenix",
     "Serving Fresno, Los Angeles &amp; California"),
    ("Serving Fresno, Los Angeles & Phoenix",
     "Serving Fresno, Los Angeles & California"),
    ("Fresno, Los Angeles &amp; Phoenix",
     "Fresno, Los Angeles &amp; California"),
    ("Fresno · Los Angeles · Phoenix",
     "Fresno · Los Angeles · California"),
]

# Meta descriptions state the service area as fact, so they move with the data.
META_AREA = [
    ("across Fresno, Los Angeles, and Phoenix",
     "across Fresno, Los Angeles, and California"),
    ("Fresno, California, and Arizona businesses",
     "Fresno and California businesses"),
]

BLOCK = re.compile(r'(<script[^>]*application/ld\+json[^>]*>)(.*?)(</script>)', re.S)


def strip_phoenix(value):
    """Drop Phoenix from an areaServed value and make sure California is in it."""
    if not isinstance(value, list):
        return value, False
    kept, dropped = [], False
    for item in value:
        name = item.get("name") if isinstance(item, dict) else item
        if isinstance(name, str) and name.strip().lower() in ("phoenix", "arizona"):
            dropped = True
            continue
        kept.append(item)
    if not dropped:
        return value, False
    structured = any(isinstance(i, dict) for i in kept)
    has_ca = any((i.get("name") if isinstance(i, dict) else i) == "California"
                 for i in kept)
    if not has_ca:
        kept.append(dict(CALIFORNIA) if structured else "California")
    return kept, True


def walk(node) -> bool:
    changed = False
    if isinstance(node, dict):
        if "areaServed" in node:
            new, hit = strip_phoenix(node["areaServed"])
            if hit:
                node["areaServed"] = new
                changed = True
        for v in node.values():
            if isinstance(v, (dict, list)):
                changed |= walk(v)
    elif isinstance(node, list):
        for v in node:
            if isinstance(v, (dict, list)):
                changed |= walk(v)
    return changed


def patch(path: Path, check: bool) -> bool:
    html = path.read_text()
    original = html

    for old, new in CONTACT_LINE + META_AREA:
        html = html.replace(old, new)

    out, last, touched = [], 0, False
    for m in BLOCK.finditer(html):
        raw = m.group(2).strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not walk(data):
            continue
        out.append(html[last:m.start(2)])
        out.append("\n" + json.dumps(data, indent=1, ensure_ascii=False) + "\n")
        last = m.end(2)
        touched = True
    if touched:
        out.append(html[last:])
        html = "".join(out)

    if html == original:
        return False
    if not check:
        path.write_text(html)
    return True


def main() -> int:
    check = "--check" in sys.argv
    hit = [p for p in sorted(ROOT.glob("*.html")) if patch(p, check)]
    if check:
        if hit:
            print(f"{len(hit)} page(s) still claim Phoenix as served: "
                  + ", ".join(p.name for p in hit))
            return 1
        print("no page claims Phoenix as a current service area")
        return 0
    print(f"corrected {len(hit)} page(s)")
    for p in hit:
        print("  ", p.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
