#!/usr/bin/env python3
"""Resolve the prose innervation strings to `data/nerves.json` ids.

    python3 scripts/seed_nerves.py           # report, with anything unresolved
    python3 scripts/seed_nerves.py --write   # apply

Innervation was 144 distinct strings and nothing could query them. A nerve is
the most conservative homology signal the dataset carries — it is what
identifies the mammalian tensor tympani as an arch 1 muscle and the stapedius as
an arch 2 one after both were relocated into the middle ear — and it was the one
criterion METHODS.md leans on that the data could not be asked about.

This adds `nerves` alongside the prose, never replacing it. Placement follows
`attachments`: on the muscle it is the consensus, on an occurrence it is what a
source records for that taxon.

The prose is kept because it says things the ids cannot: which half of a muscle
takes which nerve, that a contribution is variable, that a nerve pierces the
muscle it supplies.

MATCHING. Rules are ordered and longest-first, because "deep branch of the
radial nerve" must not resolve to the radial nerve, and "superficial fibular"
must not resolve to "fibular". Every rule is a literal substring, not a fuzzy
match, and every string that no rule claims is REPORTED rather than dropped or
guessed at — a silent partial mapping here would be worse than none, since the
missing rows would read as "this muscle has no recorded nerve".

Spinal segments (C5-C6, L2-L4) are pulled into `segments` on the row rather
than becoming nerve records: they are levels, not nerves, and they are the part
of innervation that genuinely varies between taxa.
"""

import json
import pathlib
import re
import sys

import speciesmap

ROOT = pathlib.Path(__file__).resolve().parent.parent
NERVES = ROOT / "data" / "nerves.json"
MUSCLE_FILES = sorted(ROOT.glob("data/muscles-*.json"))

# Ordered longest-first within each family. The first rule whose phrase appears
# claims that phrase; the text it matched is then blanked so a later, shorter
# rule cannot claim it again.
RULES: list[tuple[str, str]] = [
    # --- cranial, most specific first ---
    ("mandibular division of cn v", "trigeminal-mandibular"),
    ("trigeminal nerve (cn v), mandibular division", "trigeminal-mandibular"),
    ("trigeminal nerve (cn v)", "trigeminal"),
    ("cn v", "trigeminal"),
    ("facial nerve (cn vii)", "facial"),
    ("cn vii", "facial"),
    ("oculomotor (cn iii)", "oculomotor"),
    ("trochlear (cn iv)", "trochlear"),
    ("abducens (cn vi)", "abducens"),
    ("cn iii, iv, vi", "oculomotor|trochlear|abducens"),
    ("glossopharyngeal nerve (cn ix)", "glossopharyngeal"),
    ("vagus nerve (cn x)", "vagus"),
    ("caudal branchial branches of the vagus", "vagus-branchial"),
    ("vagus (x), caudal branchial branches", "vagus-branchial"),
    ("branchial vagus", "vagus-branchial"),
    ("accessory nerve (cn xi)", "accessory"),
    ("accessory nerve (xi)", "accessory"),
    ("accessory nerve equivalent", "accessory"),
    ("hypoglossal nerve (cn xii)", "hypoglossal"),
    ("hypoglossal nerve", "hypoglossal"),
    ("ansa cervicalis", "ansa-cervicalis"),
    # Bare roman numerals last, and longest first. "cn v" is a prefix of
    # "cn vii" and "cn x" of "cn xi", so a plain substring test assigned the
    # trigeminal to every facial-nerve muscle and the vagus to every accessory
    # one. The trailing guard in _pattern() is what actually prevents it; the
    # ordering keeps the intent legible.
    ("cn xii", "hypoglossal"),
    ("cn xi", "accessory"),
    ("cn x", "vagus"),
    ("cn ix", "glossopharyngeal"),
    ("cn vii", "facial"),
    ("cn vi", "abducens"),
    ("cn v", "trigeminal"),
    ("cn iv", "trochlear"),
    ("cn iii", "oculomotor"),

    # --- axial ---
    ("dorsal and ventral rami", "dorsal-rami|ventral-rami"),
    ("dorsal rami", "dorsal-rami"),
    ("ventral rami", "ventral-rami"),

    # --- brachial plexus: branches before their parents ---
    ("posterior interosseous nerve", "radial-deep"),
    ("radial nerve, posterior interosseous branch", "radial-deep"),
    ("radial nerve, deep (posterior interosseous) branch", "radial-deep"),
    ("deep branch of the radial nerve", "radial-deep"),
    ("radial nerve, deep branch", "radial-deep"),
    ("radial nerve", "radial"),
    ("anterior interosseous nerve", "median-anterior-interosseous"),
    ("median nerve, anterior interosseous branch", "median-anterior-interosseous"),
    ("recurrent branch of the median nerve", "median-recurrent"),
    ("median nerve (recurrent branch)", "median-recurrent"),
    ("median and ulnar nerves", "median|ulnar"),
    ("ulnar and median nerves", "median|ulnar"),
    ("deep branch of the ulnar nerve", "ulnar-deep"),
    ("ulnar nerve, deep branch", "ulnar-deep"),
    ("median nerve", "median"),
    ("ulnar nerve", "ulnar"),
    ("musculocutaneous nerve", "musculocutaneous"),
    ("axillary nerve", "axillary"),
    ("suprascapular nerve", "suprascapular"),
    ("supracoracoid nerve", "suprascapular"),
    ("upper and lower subscapular nerves", "subscapular"),
    ("lower subscapular / thoracodorsal nerve", "subscapular|thoracodorsal"),
    ("lower subscapular nerve", "subscapular"),
    ("subscapular nerves", "subscapular"),
    ("thoracodorsal nerve", "thoracodorsal"),
    ("thoracodorsal equivalent", "thoracodorsal"),
    ("long thoracic nerve", "long-thoracic"),
    ("dorsal scapular nerve", "dorsal-scapular"),
    ("medial and lateral pectoral nerves", "pectoral-nerves"),
    ("pectoral nerves", "pectoral-nerves"),
    ("pectoral branches arising from the ventral divisions", "pectoral-nerves"),
    ("nerve to subclavius", "nerve-to-subclavius"),
    ("dorsal (extensor) division of the brachial plexus", "brachial-dorsal-division"),
    ("ventral divisions of the brachial plexus", "brachial-ventral-division"),
    ("dorsal divisions of the brachial plexus", "brachial-dorsal-division"),
    ("anterior brachial plexus", "brachial-plexus"),
    ("brachial plexus", "brachial-plexus"),

    # --- lumbosacral plexus ---
    ("deep branch of the lateral plantar nerve", "lateral-plantar-deep"),
    ("lateral plantar nerve, deep branch", "lateral-plantar-deep"),
    ("lateral plantar nerve", "lateral-plantar"),
    ("medial plantar nerve", "medial-plantar"),
    ("deep fibular (peroneal) nerve", "deep-fibular"),
    ("deep fibular nerve", "deep-fibular"),
    ("superficial fibular nerve", "superficial-fibular"),
    ("common fibular division", "common-fibular"),
    ("common fibular nerve", "common-fibular"),
    # Unqualified "the fibular nerve" resolves to the TRUNK, not to a branch.
    # Hattori & Tsuihiji use it that way throughout — deep and superficial are
    # named where they mean them, and the sources they compile disagree about
    # which branch supplies several of these muscles, which is part of their
    # argument for not treating innervation as the decisive homology criterion.
    # Ordered after the two specific rules, which are longer and match first.
    ("fibular nerve", "common-fibular"),
    ("sciatic nerve, fibular division", "common-fibular"),
    ("sciatic nerve, tibial division", "tibial"),
    ("tibial division of the sciatic nerve", "tibial"),
    ("tibial division of the sciatic", "tibial"),
    ("sciatic nerve", "sciatic"),
    ("tibial nerve", "tibial"),
    ("superior gluteal nerve", "superior-gluteal"),
    ("inferior gluteal nerve", "inferior-gluteal"),
    ("nerve to obturator internus", "nerve-to-obturator-internus"),
    ("obturator nerve", "obturator"),
    ("femoral nerve", "femoral"),
    ("dorsal division of the lumbosacral plexus", "lumbosacral-dorsal-division"),
    ("ventral division of the lumbosacral plexus", "lumbosacral-ventral-division"),
    ("lumbosacral plexus", "lumbosacral-plexus"),
    ("lumbar plexus", "lumbosacral-plexus"),
    ("sacral plexus", "lumbosacral-plexus"),
]

# Removed BEFORE matching. These name a nerve in order to locate a HOMOLOGUE,
# not to state this muscle's supply, and a rule would read them as the latter.
# The caudofemoralis is a ventral-mass muscle on the caudal ventral rami; the
# inferior gluteal is named only to say where its mammalian counterpart ended
# up. Left in, it made the muscle look dorsally innervated — which the
# mass/division cross-check duly flagged.
PRE_STRIP = [
    "inferior gluteal nerve territory in mammals",
]

# Phrases that name no nerve and must not be reported as unresolved.
IGNORE = [
    "not spinal", "in the standard gnathostome pattern", "throughout",
    "or its non-mammalian equivalent", "spinal in origin, not branchiomeric",
    "the defining nerve of the dorsal/extensor mass", "dorsal-mass territory",
    "the dorsal/extensor division", "dorsal division", "ventral division",
    "the ventral/flexor division", "developmentally distinct from the levator",
    "scapulae, which is somitic", "with a variable radial contribution",
    "which pierces the muscle and continues as the",
    "the nerve identifies these as arch 1 derivatives even though tensor tympani",
    "lies in the middle ear", "with proprioceptive contribution from",
    "invariant across gnathostomata", "supplying the appendage",
    "in mammals", "in ambystoma also by the", "and direct branches of the",
    "direct branches", "branches of the same nerve serve the distal ischioflexorius",
    "the hamstring part of adductor magnus by the", "the ulnar half of the profundus by the",
    "the short head of biceps femoris by the", "for longus and brevis",
    "tensor fasciae latae", "longus, brevis", "tertius, digiti quinti",
    "lumbricals", "for the tongue muscles", "except palatoglossus",
    "for the infrahyoid muscles", "for rectus anterior, inferior, superior",
    "obliquus inferior, ciliaris, dilatator and sphincter pupillae",
    "transversalis oculi", "for obliquus superior", "arch 3", "arches 4",
    "stylopharyngeus by", "pharyngeal constrictors and laryngeal muscles by",
    "rectus superior, inferior, medialis, obliquus inferior, levator palpebrae",
    "rectus lateralis, retractor bulbi", "occipital and anterior spinal nerves",
    "first spinal nerve and", "first and second spinal nerves",
    "anterior caudal spinal nerves", "posterior trunk spinal nerves",
    "caudal spinal nerves", "appendicular spinal nerves", "anterior spinal nerves",
    "spinal nerves", "entering the", "typically formed from spinal nerves",
    "with considerable interspecific variation in root composition",
    "navarro et al. 2023", "in south american lizards the plexus is",
    "territory in mammals", "nerve to obturator internus in mammals",
    "branches;", "or its", "complex.", "equivalent;",
]

SEGMENT = re.compile(r"\(?\b([CTLS]\d+(?:\s*[–—-]\s*[CTLS]?\d+)?)\)?")


def _pattern(phrase):
    """A phrase must not match where a longer name continues past it.

    Without the guard, "cn v" matches inside "cn vii" and "cn x" inside
    "cn xi" — which silently gave every facial-nerve muscle a trigeminal supply
    and every accessory-nerve muscle a vagal one. Those are exactly the arch
    assignments the nerve data exists to get right, so the failure would have
    inverted the thing being demonstrated.
    """
    return re.compile(re.escape(phrase) + r"(?![a-z0-9])")


PATTERNS = [(_pattern(p), t) for p, t in RULES]


def resolve(text):
    """-> (nerve ids in order, segments string or None, leftover phrases)."""
    low = " " + text.lower() + " "

    for phrase in PRE_STRIP:
        low = low.replace(phrase, " ")

    segs = SEGMENT.findall(text)
    for s in segs:
        low = low.replace(s.lower(), " ")

    # Keyed by where the phrase sat in the text, not by rule order: the string
    # "Obturator nerve (L2-L4); ... by the tibial division of the sciatic" must
    # yield obturator first, because the segment range is the obturator's and
    # gets attached to whichever nerve leads.
    at = {}
    for pattern, target in PATTERNS:
        while (hit := pattern.search(low)):
            for nid in target.split("|"):
                at.setdefault(nid, hit.start())
            low = low[:hit.start()] + " " * (hit.end() - hit.start()) + low[hit.end():]
    ids = sorted(at, key=at.get)

    for phrase in IGNORE:
        low = low.replace(phrase, " ")

    leftover = [w for w in re.split(r"[;,.()—]|\bthe\b|\band\b|\bor\b|\bby\b|\bin\b|\bfor\b|\bof\b|\bits\b|\bwith\b|\ba\b",
                                    low) if w.strip(" -–/")]
    # Anything still containing "nerve", "plexus", "cn " or "rami" is a name no
    # rule claimed, which is the case worth surfacing.
    missed = [w.strip() for w in leftover
              if re.search(r"nerv|plexus|\bcn\b|ram[ui]|branch", w)]

    return ids, ("; ".join(dict.fromkeys(segs)) or None), missed


def main():
    write = "--write" in sys.argv
    valid = {n["id"] for n in json.loads(NERVES.read_text())["nerves"]}

    bad = {t for _, target in RULES for t in target.split("|") if t not in valid}
    if bad:
        sys.exit(f"seed error: rules target unknown nerve ids {sorted(bad)}")

    docs = {p: json.loads(p.read_text()) for p in MUSCLE_FILES}
    applied = unchanged = 0
    unresolved = []

    for path, doc in docs.items():
        for m in doc["muscles"]:
            holders = [(m, (m.get("consensus") or {}).get("innervation"), "consensus")]
            for o in m.get("occurrences", []):
                holders.append((o, o.get("innervation"), speciesmap.clade_of(o)))

            for holder, text, tag in holders:
                if not text:
                    continue
                ids, segs, missed = resolve(text)
                if missed:
                    unresolved.append(f"{m['id']}/{tag}: {'; '.join(missed)}  <- {text[:70]}")
                if not ids:
                    continue
                # Seed, not sync. Carrying the notes across was not enough: the
                # rows themselves were rebuilt from the prose every run, and the
                # parser is coarser than the curator. It was demoting
                # `median-anterior-interosseous` to `median`, and `obturator`,
                # `nerve-to-obturator-internus` and `tibial` all to
                # `lumbosacral-plexus`, on rows somebody had resolved by hand.
                # A row that already has nerves is finished; parse only the
                # prose that has none.
                if holder.get("nerves"):
                    unchanged += 1
                    continue
                # Notes are hand-added — the seed derives ids and segments, not
                # commentary — so carry them across by nerve id. Without this,
                # re-running the seed silently discards curation, which is the
                # failure mode that makes people stop re-running seeds.
                kept = {r["nerve"]: r["note"] for r in (holder.get("nerves") or [])
                        if isinstance(r, dict) and r.get("note")}
                rows = [{"nerve": i} for i in ids]
                for row in rows:
                    if row["nerve"] in kept:
                        row["note"] = kept[row["nerve"]]
                # Only pair segments with a nerve where the pairing is
                # unambiguous. "CN XII for the tongue muscles ...; ansa
                # cervicalis (C1-C3)" names two nerves and one range, and the
                # range is the second nerve's — attaching it to the first
                # would invent a claim. The prose is kept, so nothing is lost.
                if segs and len(rows) == 1:
                    rows[0]["segments"] = segs
                if holder.get("nerves") == rows:
                    unchanged += 1
                    continue
                applied += 1
                if write:
                    holder["nerves"] = rows

    for line in sorted(unresolved):
        print(f"  UNRESOLVED {line}")

    print(f"\n{applied} rows to apply, {unchanged} already current, "
          f"{len(unresolved)} strings with an unclaimed nerve name")

    if write and applied:
        for path, doc in docs.items():
            path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        print(f"wrote {len(docs)} files")
    elif not write:
        print("(dry run — pass --write to apply)")

    # An innervation string the parser cannot place is a gap in `nerves.json`,
    # not a broken build — the same standing as validate.py's never-cited
    # sources. Returning 1 here stopped `build.sh` dead at step 12 on all 71 of
    # them, so no later step ran. Report and carry on; validate.py is the gate.
    return 0


if __name__ == "__main__":
    sys.exit(main())
