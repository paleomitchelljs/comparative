#!/usr/bin/env python3
"""Seed taxon-specific `attachments` on occurrence rows.

Muscle-level `attachments` is a consensus. It cannot express the thing that is
often the actual result — that a muscle's attachment MOVED. This adds structured
per-taxon attachments for cases the sources document explicitly, so the app can
diff them against the plesiomorphic condition and surface the shift.

Only documented shifts are seeded. Occurrences left alone inherit the consensus,
and the app marks them as inherited rather than observed. Every entry below
carries the source that supports it.

    python3 scripts/seed_occurrence_attachments.py           # report
    python3 scripts/seed_occurrence_attachments.py --write   # apply
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# muscle id -> taxon id -> {origin, insertion, sources, shiftNote}
SEED = {
    "supracoracoideus": {
        "caudata":      {"origin": ["coracoid", "scapula"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "testudines":   {"origin": ["coracoid", "scapula"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "lepidosauria": {"origin": ["coracoid", "scapula"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "crocodylia":   {"origin": ["coracoid", "scapula"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "aves": {"origin": ["sternal-keel"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"],
                 "shiftNote": "Origin restricted to the sternal keel and the tendon rerouted dorsally through the foramen triosseum, so a ventrally placed muscle produces the upstroke."},
        "monotremata": {"origin": ["coracoid", "scapula"], "insertion": ["greater-tubercle"], "sources": ["gambaryan-etal-2015", "fahn-lai-etal-2020"],
                        "shiftNote": "The scapular spine is only incipient, so the supracoracoideus field is just beginning to divide into supraspinatus and infraspinatus. The readable intermediate."},
        "theria": {"origin": ["supraspinous-fossa", "infraspinous-fossa"], "insertion": ["greater-tubercle"], "sources": ["ercoli-etal-2014", "fahn-lai-etal-2020"],
                   "shiftNote": "Origin has migrated off the coracoid — which no longer exists as a separate bone — onto the lateral scapula, where the new scapular spine splits it into supraspinatus and infraspinatus."},
    },
    "subcoracoscapularis": {
        "testudines":   {"origin": ["scapula", "coracoid"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "lepidosauria": {"origin": ["scapula", "coracoid"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "crocodylia":   {"origin": ["scapula", "coracoid"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "aves":         {"origin": ["scapula", "coracoid"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "theria": {"origin": ["subscapular-fossa"], "insertion": ["lesser-tubercle"], "sources": ["ercoli-etal-2014"],
                   "shiftNote": "The coracoid head is gone with the coracoid itself; only the scapular head persists, which is why the mammalian muscle is 'subscapularis' rather than 'subcoraco-scapularis'."},
    },
    "pectoralis": {
        "caudata":    {"origin": ["sternum", "body-wall"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "lepidosauria": {"origin": ["sternum", "interclavicle", "ribs"], "insertion": ["deltopectoral-crest"], "sources": ["abdala-diogo-2010", "freitas-etal-2017"]},
        "aves": {"origin": ["sternal-keel", "furcula"], "insertion": ["deltopectoral-crest"], "sources": ["abdala-diogo-2010"],
                 "shiftNote": "Origin concentrated on the carina; the largest muscle in the body of most flying birds."},
        "monotremata": {"origin": ["sternum", "interclavicle", "clavicle"], "insertion": ["deltopectoral-crest"], "sources": ["gambaryan-etal-2015"],
                        "shiftNote": "More extensive origin than in therians because monotremes retain the interclavicle."},
        "theria": {"origin": ["sternum", "clavicle", "ribs"], "insertion": ["greater-tubercle"], "sources": ["ercoli-etal-2014"]},
    },
    "deltoideus-clavicularis": {
        "caudata":      {"origin": ["procoracoid"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"],
                         "shiftNote": "Called procoracohumeralis in amphibians purely because the origin sits on the procoracoid."},
        "anura":        {"origin": ["procoracoid"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "testudines":   {"origin": ["clavicle"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "lepidosauria": {"origin": ["clavicle"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "crocodylia": {"origin": ["scapula"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"],
                       "shiftNote": "Crocodylians have no clavicle, so despite the name the origin sits on the scapula — which is why Fürbringer (1876) called this muscle the scapularis inferior."},
        "theria": {"origin": ["acromion", "clavicle"], "insertion": ["deltopectoral-crest"], "sources": ["ercoli-etal-2014"],
                   "shiftNote": "The muscle is renamed at every step for the bone that happens to carry its origin, though the muscle itself is continuous across Tetrapoda."},
    },
    "extensor-antebrachii-carpi-radialis": {
        "caudata": {"origin": ["lateral-epicondyle"], "insertion": ["radius", "carpals"], "sources": ["abdala-diogo-2010"],
                    "shiftNote": "Plesiomorphic tetrapod condition: insertion stops at the radius and proximal carpals."},
        "anura": {"origin": ["lateral-epicondyle"], "insertion": ["metacarpals"], "sources": ["abdala-diogo-2010"],
                  "shiftNote": "In Phyllomedusa and other grasping tree frogs the insertion has shifted distally onto the metacarpals — the same shift mammals made, independently."},
        "testudines":   {"origin": ["lateral-epicondyle"], "insertion": ["radius", "carpals"], "sources": ["abdala-diogo-2010"]},
        "lepidosauria": {"origin": ["lateral-epicondyle"], "insertion": ["radius", "carpals"], "sources": ["abdala-diogo-2010"]},
        "crocodylia":   {"origin": ["lateral-epicondyle"], "insertion": ["radius", "carpals"], "sources": ["abdala-diogo-2010"]},
        "theria": {"origin": ["supracondylar-ridge", "lateral-epicondyle"], "insertion": ["metacarpals"], "sources": ["ercoli-etal-2014"],
                   "shiftNote": "Distal migration onto the metacarpals, correlated with finer digital control — and convergent with the anuran condition."},
    },
    "latissimus-dorsi": {
        "caudata":    {"origin": ["body-wall"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "testudines": {"origin": ["ribs"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"],
                       "shiftNote": "Origin transferred onto the internal surface of the carapace, which is built from the ribs."},
        "theria": {"origin": ["thoracolumbar-fascia", "thoracic-neural-spines", "ribs"], "insertion": ["humerus"], "sources": ["ercoli-etal-2014"]},
    },
    "sternocoracoideus": {
        "lepidosauria": {"origin": ["sternum"], "insertion": ["coracoid"], "sources": ["abdala-diogo-2010"]},
        "aves":         {"origin": ["sternum"], "insertion": ["coracoid"], "sources": ["abdala-diogo-2010"]},
        "monotremata":  {"origin": ["sternum"], "insertion": ["coracoid"], "sources": ["gambaryan-etal-2015"]},
        "theria": {"origin": ["ribs"], "insertion": ["clavicle"], "sources": ["abdala-diogo-2010"],
                   "shiftNote": "As the subclavius. With the coracoid gone the insertion transfers to the clavicle — Howell's (1937b) basis for the homology."},
    },
    "caudofemoralis": {
        "lepidosauria": {"origin": ["caudal-vertebrae", "ilium"], "insertion": ["fourth-trochanter"], "sources": ["diogo-molnar-2014"],
                         "shiftNote": "Inserts on the fourth trochanter, whose size reads directly as femoral-retractor power."},
        "crocodylia":   {"origin": ["caudal-vertebrae", "ilium"], "insertion": ["fourth-trochanter"], "sources": ["diogo-molnar-2014", "allen-etal-2014"]},
        "testudines":   {"origin": ["caudal-vertebrae"], "insertion": ["femur"], "sources": ["diogo-molnar-2014"]},
        "synapsida-stem": {"origin": ["caudal-vertebrae"], "insertion": ["fourth-trochanter"], "sources": ["bishop-pierce-2024"],
                           "shiftNote": "Progressive reduction of the fourth trochanter along the synapsid stem tracks the loss of tail-driven femoral retraction."},
    },
    "opercularis": {
        "anura": {"origin": ["suprascapula"], "insertion": ["operculum"], "sources": ["abdala-diogo-2010"],
                  "shiftNote": "A pectoral girdle muscle inserting on the ear. Anuran-only, and only in anurans is it a discrete muscle."},
    },
    "triceps-brachii": {
        "caudata":    {"origin": ["scapula", "humerus"], "insertion": ["olecranon"], "sources": ["abdala-diogo-2010"]},
        "lepidosauria": {"origin": ["scapula", "coracoid", "humerus"], "insertion": ["olecranon"], "sources": ["abdala-diogo-2010"]},
        "theria": {"origin": ["scapula", "humerus"], "insertion": ["olecranon"], "sources": ["ercoli-etal-2014"]},
    },
    "biceps-brachii": {
        "lepidosauria": {"origin": ["coracoid"], "insertion": ["radius"], "sources": ["abdala-diogo-2010"]},
        "theria": {"origin": ["scapula", "coracoid-process"], "insertion": ["radial-tuberosity"], "sources": ["ercoli-etal-2014"],
                   "shiftNote": "The short head arises from the coracoid process — the fused remnant of the coracoid — rather than from a coracoid bone."},
    },
    "coracobrachialis": {
        "caudata":      {"origin": ["coracoid"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "lepidosauria": {"origin": ["coracoid"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "aves":         {"origin": ["coracoid"], "insertion": ["humerus"], "sources": ["abdala-diogo-2010"]},
        "theria": {"origin": ["coracoid-process"], "insertion": ["humerus"], "sources": ["ercoli-etal-2014"],
                   "shiftNote": "Origin transfers to the coracoid process as the coracoid bone is lost."},
    },
    "hypobranchial-muscles": {
        "chondrichthyes": {"origin": ["pectoral-girdle"], "insertion": ["mandible", "hyoid", "branchial-arches"], "sources": ["ziermann-etal-2014", "diogo-ziermann-2015"],
                           "shiftNote": "Origin on the coracoid bar ties the feeding apparatus mechanically to the pectoral girdle. Loosening that link is a precondition for a neck."},
        "theria": {"origin": ["sternum", "clavicle", "scapula", "hyoid"], "insertion": ["hyoid", "tongue"], "sources": ["ziermann-diogo-2019"],
                   "shiftNote": "With the coracoid gone the infrahyoid muscles take origin from sternum, clavicle and scapula instead."},
    },
    "iliofemoralis": {
        "lepidosauria": {"origin": ["ilium"], "insertion": ["femur"], "sources": ["diogo-molnar-2014"]},
        "synapsida-stem": {"origin": ["ilium", "iliac-crest"], "insertion": ["greater-trochanter"], "sources": ["bishop-pierce-2024"],
                           "shiftNote": "Expansion of the iliac blade along the synapsid stem tracks the enlargement of this field and the shift toward erect posture."},
        "theria": {"origin": ["ilium", "iliac-crest"], "insertion": ["greater-trochanter"], "sources": ["diogo-molnar-2014"],
                   "shiftNote": "Same muscle, same nerve, same attachments — but in a parasagittal limb it becomes the principal pelvic stabiliser during single-limb support."},
    },
}


def main(write: bool) -> int:
    skel = json.loads((ROOT / "data/skeleton.json").read_text())
    elements = {e["id"]: e for e in skel["elements"]}

    docs, added, problems = {}, 0, []
    index = {}
    for path in sorted(ROOT.glob("data/muscles-*.json")):
        doc = json.loads(path.read_text())
        docs[path] = doc
        for m in doc["muscles"]:
            index[m["id"]] = m

    for mid, per_taxon in SEED.items():
        m = index.get(mid)
        if not m:
            problems.append(f"unknown muscle '{mid}'")
            continue
        occs = {o["taxon"]: o for o in m.get("occurrences", [])}
        for tid, spec in per_taxon.items():
            occ = occs.get(tid)
            if not occ:
                problems.append(f"{mid}: no occurrence row for taxon '{tid}'")
                continue
            for side in ("origin", "insertion"):
                for ref in spec.get(side, []):
                    if ref not in elements:
                        problems.append(f"{mid}/{tid}: '{ref}' not in skeleton.json")
                        continue
                    pres = elements[ref].get("presence", {})
                    ok = tid not in pres.get("absent", []) and (
                        pres.get("default") != "no"
                        or tid in pres.get("present", []) + pres.get("partial", []) + pres.get("reduced", []))
                    if not ok:
                        problems.append(f"{mid}/{tid}: '{ref}' is recorded absent in that taxon")
            occ["attachments"] = {"origin": spec["origin"], "insertion": spec["insertion"]}
            if spec.get("shiftNote"):
                occ["attachmentNote"] = spec["shiftNote"]
            occ["sources"] = sorted(set(occ.get("sources", [])) | set(spec["sources"]))
            added += 1

    if problems:
        print("PROBLEMS:")
        for p in problems:
            print(f"  {p}")
        return 1

    print(f"{added} occurrence rows seeded with structured attachments "
          f"across {len(SEED)} muscles")

    if not write:
        print("\nDry run. Re-run with --write to apply.")
        return 0

    for path, doc in docs.items():
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    print(f"rewrote {len(docs)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main("--write" in sys.argv))
