#!/usr/bin/env python3
"""Extract Werneburg (2011) Appendix 1 into a local working file.

Werneburg's Appendix 1 is a 94-entry structured catalogue of turtle cranial
muscular units, each with origin, insertion, function, innervation and a synonym
list going back to Bojanus (1819-21). It is by far the densest per-muscle source
in papers/, and the only one whose layout survives `pdftotext -layout` cleanly.

This script parses that appendix into JSON so a curator can work from structured
records rather than scrolling a 99-page PDF.

    python3 scripts/extract_werneburg_appendix.py

Output goes to data/raw/werneburg-2011-appendix1.json, which is git-ignored.
That is deliberate: the output holds the source's own wording, and the committed
dataset under data/muscles-*.json contains paraphrased entries with citations
instead. Use this file as a reading aid when curating, not as a data feed.

Requires the PDF at papers/2011_Werneburg_Testudines_Extant_cranial-musculature.pdf
and `pdftotext` (poppler) on PATH.
"""

import json
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PDF = ROOT / "papers/2011_Werneburg_Testudines_Extant_cranial-musculature.pdf"
OUT = ROOT / "data/raw/werneburg-2011-appendix1.json"

# Appendix rows are label-prefixed continuation blocks: a bare keyword in column
# zero, then wrapped text indented under it.
FIELDS = ("origin", "insertion", "function", "synonyms", "comments")
FIELD_RE = re.compile(rf"^({'|'.join(FIELDS)})\s+(.*)$")

# "12*  m. nasalis   m. nasITENAR   V" — number, name, abbreviation, nerve.
# Asterisks (one or two) mark entries flagged in Werneburg's figures. A few
# headers cover a group of units and carry a range instead of a single number
# ("31-33/42  'm. inter-mandibularis' complex  -  V / VII").
HEADER_RE = re.compile(
    r"^(?P<no>\d{1,3})(?P<range>[-–/]\d{1,3}(?:[-–/]\d{1,3})*)?(?P<flag>\*{0,2})\s{2,}"
    r"(?P<name>\S.*?)\s{2,}"
    r"(?P<abbr>\S.*?)\s{2,}"
    r"(?P<nerve>[IVX]+(?:\s*[/+,]\s*[IVX]+)*|C\d.*?)\s*$"
)

NOISE = re.compile(
    r"^\s*(PALAEO-ELECTRONICA\.ORG|WERNEBURG: CRANIAL TURTLE MUSCULATURE|"
    r"No\.\s+muscle name|\d{1,3}\s*$)"
)


def pdf_to_text() -> str:
    if not PDF.exists():
        sys.exit(f"missing PDF: {PDF.relative_to(ROOT)}\n"
                 "The PDFs are git-ignored; this script only runs where they are present.")
    if not shutil.which("pdftotext"):
        sys.exit("pdftotext not found. Install poppler (brew install poppler).")
    return subprocess.run(
        ["pdftotext", "-layout", str(PDF), "-"],
        capture_output=True, text=True, check=True,
    ).stdout


def parse(text: str) -> list[dict]:
    lines = text.splitlines()

    start = next((i for i, l in enumerate(lines) if "APPENDIX 1." in l), None)
    end = next((i for i, l in enumerate(lines) if "APPENDIX 2." in l), len(lines))
    if start is None:
        sys.exit("could not locate 'APPENDIX 1.' — the PDF layout may differ")

    records: list[dict] = []
    current: dict | None = None
    field: str | None = None

    for raw in lines[start:end]:
        line = raw.rstrip()
        if not line.strip() or NOISE.match(line):
            continue

        header = HEADER_RE.match(line.strip())
        if header and not FIELD_RE.match(line.strip()):
            current = {
                "no": int(header["no"]),
                "span": (header["no"] + header["range"]) if header["range"] else None,
                "flagged": bool(header["flag"]),
                "name": header["name"].strip(),
                "abbreviation": header["abbr"].strip(),
                "innervation": header["nerve"].strip(),
                **{f: "" for f in FIELDS},
            }
            records.append(current)
            field = None
            continue

        if current is None:
            continue

        m = FIELD_RE.match(line.strip())
        if m:
            field = m[1]
            current[field] = m[2].strip()
        elif field:
            # Continuation of the previous field's wrapped text.
            current[field] = (current[field] + " " + line.strip()).strip()
        elif line.startswith(" " * 8) and not current["origin"]:
            # A "Pars ..." qualifier printed under the muscle name.
            current["name"] += " — " + line.strip()

    for r in records:
        r["synonyms"] = [s.strip() for s in re.split(r",(?![^()]*\))", r["synonyms"]) if s.strip()]

    return records


def main() -> int:
    records = parse(pdf_to_text())
    if not records:
        sys.exit("parsed zero records — check that the PDF text layer is intact")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(
        {
            "source": "werneburg-2011",
            "citation": "Werneburg I. 2011. The cranial musculature of turtles. "
                        "Palaeontologia Electronica 14(2):15A, Appendix 1.",
            "warning": "Verbatim extraction for curation use only. Do not commit; "
                       "paraphrase into data/muscles-*.json with a citation.",
            "count": len(records),
            "records": records,
        },
        indent=2, ensure_ascii=False) + "\n")

    with_oi = sum(1 for r in records if r["origin"] and r["insertion"])
    nerves = sorted({r["innervation"] for r in records if r["innervation"]})
    print(f"parsed {len(records)} muscular units ({with_oi} with both origin and insertion)")
    print(f"innervation values seen: {', '.join(nerves)}")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
