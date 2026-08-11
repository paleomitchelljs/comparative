#!/usr/bin/env python3
"""Crocodylian limb attachments from Klinkhamer et al. (2017).

    python3 scripts/seed_klinkhamer_crocodylus.py [--write]

The coverage audit put Crocodylia at 19 muscles away from a computable
attachment shift, with the forearm and hand at one scored row apiece. Klinkhamer
et al. digitally dissected Crocodylus porosus and describe an origin and an
insertion for every limb muscle they segmented, which is exactly the shape of
data the occurrence rows want.

Only muscles whose identity in this dataset is unambiguous are seeded. Several
of their muscles are crocodylian subdivisions with no single counterpart here
(coracobrachialis brevis dorsalis/ventralis, the three triceps heads, the two
gastrocnemius bellies) — those are folded into the homology group where the
group is what this dataset records, and left alone where folding would assert a
correspondence the paper does not make.

Terms are as reported. Where the paper's description is coarser than this
dataset's landmarks ("the ventral manus", "the dorsal manus") the row stops at
the bone, per the rule in METHODS.md that an ambiguous term asserts no landmark.
"""
import json, pathlib, sys

import speciesmap

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ["klinkhamer-etal-2017"]

def r(element, side=None, landmark=None):
    row = {"element": element}
    if side: row["side"] = side
    if landmark: row["landmark"] = landmark
    return row

SEED = {
 "pectoralis": (
   [r("interclavicle"), r("sternum"), r("ribs", "ventral")],
   [r("humerus", "proximal", "deltopectoral-crest")],
   "Fleshy along the ventral midline from interclavicle and sternal ribs; "
   "tendinous onto the deltopectoral crest."),
 "teres-major": (
   [r("scapula", "lateral", "subscapular-fossa")],
   [r("humerus", "proximal")],
   "Origin fleshy on the distolateral scapula; a long well-defined tendon to a "
   "bony ridge on the proximolateral humerus — a scar worth looking for in "
   "fossil pseudosuchians."),
 "deltoideus-scapularis": (
   [r("scapula", "lateral")],
   [r("humerus", "dorsal", "deltopectoral-crest")],
   "Fleshy on the distolateral scapula, tendinous on the dorsolateral humeral "
   "head."),
 "subcoracoscapularis": (
   [r("scapula", "posterior")],
   [r("humerus", "dorsal")],
   "Reported as subscapularis: fleshy at both ends, posterolateral scapula to "
   "dorsolateral humeral head."),
 "coracobrachialis": (
   [r("coracoid", "lateral")],
   [r("humerus", "proximal", "deltopectoral-crest")],
   "Klinkhamer et al. divide this into brevis ventralis and brevis dorsalis. "
   "The ventralis is scored here — fleshy over the entire lateral coracoid to "
   "the deltopectoral crest. They give the dorsalis an anterolateral SCAPULAR "
   "origin, which is not a coracoid attachment and is not folded in."),
 "biceps-brachii": (
   [r("coracoid", "ventral")],
   [r("radius", "proximal")],
   "A very long tendon of origin from the ventral coracoid — about half the "
   "length of the belly — to the proximomedial radius."),
 "brachialis": (
   [r("humerus", "anterior")],
   [r("radius", "proximal")],
   "Fleshy on the anterior humeral head; inserts on the proximomedial radius "
   "with the biceps tendon."),
 "humeroradialis": (
   [r("humerus", "ventral", "deltopectoral-crest")],
   [r("radius", "proximal")],
   "Fleshy from the deltopectoral crest, inserting with biceps and brachialis."),
 "triceps-brachii": (
   [r("scapula", "proximal"), r("humerus", "proximal")],
   [r("ulna", "proximal", "olecranon")],
   "Three heads: longus lateralis and longus medialis from the proximolateral "
   "scapula, brevis fleshy on the proximolateral humerus. All converge on the "
   "olecranon."),
 "flexor-carpi-ulnaris": (
   [r("humerus", "distal", "medial-epicondyle")],
   [r("carpals", "ventral")],
   "Tendinous at the distomedial humerus, fleshy at the ventral carpus."),
 "flexor-digitorum-longus": (
   [r("humerus", "distal", "medial-epicondyle")],
   [r("phalanges-manus")],
   "Tendinous at both ends; reaches digit 2 of the manus."),
 "extensor-antebrachii-carpi-ulnaris": (
   [r("humerus", "distal", "lateral-epicondyle")],
   [r("metacarpals", "dorsal")],
   "Reported as extensor carpi ulnaris, tendinous from the lateral condyle to "
   "the dorsal manus."),
 "extensor-antebrachii-carpi-radialis": (
   [r("humerus", "ventral"), r("ulna", "proximal"), r("radius", "proximal")],
   [r("metacarpals", "dorsal")],
   "Longus from the ventrolateral humerus; brevis by two nearly indistinct "
   "heads on the proximal ulna and radius."),
 "pronator-teres": (
   [r("humerus", "distal", "medial-epicondyle")],
   [r("carpals", "ventral")],
   "Tendinous at the ventrodistal humerus, fleshy on the ventral carpus. Note "
   "the carpal rather than radial insertion — Klinkhamer et al. report it that "
   "way for Crocodylus."),
 "pronator-quadratus": (
   [r("ulna", "proximal")],
   [r("radius", "distal")],
   "Fleshy at the proximomedial ulna to the posterodistal radius."),
 "adductor-femoris": (
   [r("ischium", "ventral")],
   [r("femur", "ventral")],
   "Fleshy at the ventrolateral ischium, tendinous at the ventromedial femur."),
}
def main():
    write = "--write" in sys.argv
    applied = skipped = 0
    for path in sorted(ROOT.glob("data/muscles-*.json")):
        doc = json.loads(path.read_text()); touched = False
        for m in doc["muscles"]:
            spec = SEED.get(m["id"])
            if not spec: continue
            occ = next((o for o in m["occurrences"] if speciesmap.clade_of(o) == "crocodylia"), None)
            if occ is None:
                print(f"  MISS  {m['id']}: no crocodylia occurrence"); continue
            if occ.get("attachments"):
                skipped += 1; continue
            origin, insertion, note = spec
            occ["attachments"] = {"origin": origin, "insertion": insertion}
            occ["attachmentNote"] = note
            occ["sources"] = sorted(set(occ.get("sources", [])) | set(SRC))
            if "klinkhamer-etal-2017" not in m["sources"]:
                m["sources"] = sorted(set(m["sources"]) | set(SRC))
            applied += 1; touched = True
            print(f"  + {m['id']}")
        if touched and write:
            path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    print(f"\n{applied} rows seeded, {skipped} already had attachments")
    if not write: print("(dry run — pass --write to apply)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
