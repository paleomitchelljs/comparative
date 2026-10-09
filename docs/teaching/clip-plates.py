#!/usr/bin/env python3
r"""Clip the figure plates used by skull-id-figures.tex out of the local PDFs.

The PDFs in `papers/` are git-ignored and so is the `plates/` directory this
writes into: the plates are reproduced from the literature under the licences
listed in PLATES below, and this repository does not redistribute them. Run
this locally, with the PDFs present, and the guide picks the plates up.
Without them the guide still compiles -- every \includegraphics is guarded by
\IfFileExists, and the schematic figures are drawn in TikZ and always present.

    python3 docs/teaching/clip-plates.py            # write docs/teaching/plates/
    python3 docs/teaching/clip-plates.py --list     # print the plate list only

Requires pdftoppm (poppler) and Pillow.
"""

import argparse
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = pathlib.Path(__file__).resolve().parent / "plates"
DPI = 400

# Crops are page fractions (left, top, right, bottom), so they survive a change
# of DPI. `licence` is what governs reuse; `credit` is the line the guide prints
# under the plate, and it is not optional under any of these licences.
PLATES = [
    dict(
        name="temporal-terminology-tuatara",
        pdf="papers/2024_Werneburg-Preuschoft_Tetrapoda_Phanerozoic_temporal-fenestrae-biomechanics.pdf",
        page=5,
        crop=(0.070, 0.058, 0.935, 0.487),
        licence="CC BY-NC 4.0",
        credit="Werneburg \\& Preuschoft (2024), Anat.\\ Rec.\\ 307:1559--1593, "
               "fig.~1a. CC BY-NC 4.0.",
        what="Sphenodon skull, lateral. Every roofing bone named; both temporal "
             "fenestrae and all the bars colour-coded.",
    ),
    dict(
        name="temporal-terminology-turtle",
        pdf="papers/2024_Werneburg-Preuschoft_Tetrapoda_Phanerozoic_temporal-fenestrae-biomechanics.pdf",
        page=5,
        crop=(0.070, 0.482, 0.935, 0.900),
        licence="CC BY-NC 4.0",
        credit="Werneburg \\& Preuschoft (2024), Anat.\\ Rec.\\ 307:1559--1593, "
               "fig.~1b. CC BY-NC 4.0.",
        what="Chelydra skull, lateral. The same labels on an emarginate skull -- "
             "the direct comparison that makes emargination legible.",
    ),
    dict(
        name="skull-morphotypes-tree",
        pdf="papers/2024_Werneburg-Preuschoft_Tetrapoda_Phanerozoic_temporal-fenestrae-biomechanics.pdf",
        page=28,
        crop=(0.060, 0.055, 0.945, 0.865),
        licence="CC BY-NC 4.0",
        credit="Werneburg \\& Preuschoft (2024), Anat.\\ Rec.\\ 307:1559--1593, "
               "fig.~18. CC BY-NC 4.0.",
        what="Temporal morphotypes on a tetrapod tree. ADVANCED: uses the "
             "authors' own nine-term morphotype scheme, not anapsid/synapsid/"
             "diapsid. Do not hand this to a beginner unlabelled.",
    ),
    dict(
        name="bird-skull-pigeon",
        pdf="papers/2019_Jones-Button-Barrett-Porro_Aves-Columbidae_Extant_head-digital-dissection.pdf",
        page=8,
        crop=(0.095, 0.105, 0.910, 0.345),
        licence="CC BY 4.0",
        credit="Jones, Button, Barrett \\& Porro (2019), Zool.\\ Lett.\\ 5:17, "
               "fig.~3a. CC BY 4.0.",
        what="Columba livia skull, lateral, from micro-CT. Beak, huge orbit, "
             "confluent temporal region, fused braincase.",
    ),
    dict(
        name="bird-skull-pigeon-quadrate",
        pdf="papers/2019_Jones-Button-Barrett-Porro_Aves-Columbidae_Extant_head-digital-dissection.pdf",
        page=8,
        crop=(0.095, 0.350, 0.910, 0.560),
        licence="CC BY 4.0",
        credit="Jones, Button, Barrett \\& Porro (2019), Zool.\\ Lett.\\ 5:17, "
               "fig.~3b. CC BY 4.0.",
        what="The same skull, dorsolateral, with the quadrate picked out in "
             "colour and the interorbital septum labelled -- the two things that "
             "make avian kinesis make sense.",
    ),
]


def clip(spec, out_dir):
    pdf = ROOT / spec["pdf"]
    if not pdf.exists():
        return None, f"missing PDF: {spec['pdf']}"
    try:
        from PIL import Image
    except ImportError:
        return None, "Pillow is not installed (pip install Pillow)"

    stem = out_dir / f"_page_{spec['name']}"
    subprocess.run(
        ["pdftoppm", "-r", str(DPI), "-png", "-f", str(spec["page"]),
         "-l", str(spec["page"]), str(pdf), str(stem)],
        check=True, capture_output=True,
    )
    rendered = sorted(out_dir.glob(f"_page_{spec['name']}*.png"))
    if not rendered:
        return None, "pdftoppm produced nothing"
    page = rendered[0]
    im = Image.open(page)
    w, h = im.size
    l, t, r, b = spec["crop"]
    im.crop((int(l * w), int(t * h), int(r * w), int(b * h))).save(
        out_dir / f"{spec['name']}.png", optimize=True
    )
    page.unlink()
    return f"{spec['name']}.png", None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", action="store_true", help="print the plate list and exit")
    args = ap.parse_args()

    if args.list:
        for s in PLATES:
            print(f"{s['name']}\n    {s['pdf']} p.{s['page']}  [{s['licence']}]\n"
                  f"    {s['what']}\n")
        return 0

    OUT.mkdir(exist_ok=True)
    ok, bad = [], []
    for spec in PLATES:
        name, err = clip(spec, OUT)
        (bad if err else ok).append(f"{spec['name']}: {err}" if err else name)
    for n in ok:
        print(f"  wrote plates/{n}")
    for e in bad:
        print(f"  SKIPPED {e}", file=sys.stderr)
    if not ok:
        print("\nNo plates written. The guide still compiles without them.",
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
