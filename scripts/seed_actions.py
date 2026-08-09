#!/usr/bin/env python3
"""Resolve action prose to {joint, motion} rows against data/joints.json.

    python3 scripts/seed_actions.py           # report, listing what it will not claim
    python3 scripts/seed_actions.py --write   # apply

Action was 121 distinct strings for 126 records and could not be searched,
faceted or compared. Now that joints exist, an action has somewhere to point:
"flexes the femur-tibia joint" rather than a sentence.

The prose stays. It carries the qualifications that matter — that an action
holds only in sprawling posture, that a muscle stabilises rather than moves,
that its line of action reverses with limb position — and none of that survives
reduction to a verb.

CONSERVATIVE BY DESIGN. A rule fires only where a motion verb and a moved
segment appear in the same clause, and the joint follows from the segment: a
muscle that "abducts the femur" acts at the hip, because the femur is the bone
distal to it. Anything else is REPORTED, not guessed. Roughly a third of the
strings describe compound or postural effects that no rule should try to reduce,
and a wrong action is worse than a missing one — it would be indexed, faceted
and counted as though someone had asserted it.

The joint graph then checks the result: an action's joint should be one the
muscle actually crosses, given its attachments. That check is the reason to
derive crossings rather than store them, and it caught real errors on the first
run.
"""

import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import jointgraph

ROOT = pathlib.Path(__file__).resolve().parent.parent
JOINTS = ROOT / "data" / "joints.json"
MUSCLE_FILES = sorted(ROOT.glob("data/muscles-*.json"))

# What is being moved -> the joint it moves at. The joint is the one immediately
# proximal to the named segment, which is what "flexes the femur" means.
SEGMENT_JOINT = [
    ("mandible", "jaw-joint"), ("jaw", "jaw-joint"), ("lower jaw", "jaw-joint"),
    ("head", "craniovertebral"), ("skull", "craniovertebral"),
    ("rib", "costovertebral"),
    ("vertebral column", "intervertebral"), ("trunk", "intervertebral"),
    ("tail", "intervertebral"), ("body", "intervertebral"),
    ("pectoral girdle", "girdle-axial"), ("scapula", "girdle-axial"),
    ("clavicle", "girdle-axial"), ("girdle", "girdle-axial"),
    ("glenohumeral", "shoulder"), ("shoulder", "shoulder"),
    ("humerus", "shoulder"), ("arm", "shoulder"), ("forelimb", "shoulder"),
    ("antebrachium", "elbow"), ("forearm", "elbow"), ("elbow", "elbow"),
    ("radius", "radioulnar"),
    ("wrist", "wrist"), ("carpus", "wrist"), ("hand", "wrist"), ("manus", "wrist"),
    ("thumb", "carpometacarpal"), ("pollex", "carpometacarpal"),
    ("femur", "hip"), ("thigh", "hip"), ("hip", "hip"), ("hindlimb", "hip"),
    ("crus", "knee"), ("shank", "knee"), ("knee", "knee"), ("tibia", "knee"),
    ("leg", "knee"),
    ("ankle", "ankle"), ("foot", "ankle"), ("pes", "ankle"), ("tarsus", "ankle"),
    # A joint named outright, which several strings do.
    ("metacarpophalangeal", "metacarpophalangeal"),
    ("interphalangeal", "interphalangeal-manus"),
    ("metatarsophalangeal", "metatarsophalangeal"),
    ("carpometacarpal", "carpometacarpal"),
    ("tarsometatarsal", "tarsometatarsal"),
    ("radioulnar", "radioulnar"), ("tibiofibular", "tibiofibular"),
    ("sacroiliac", "sacroiliac"), ("costovertebral", "costovertebral"),
    ("intervertebral", "intervertebral"),
    ("suspensorium", "suspensorium"), ("palatoquadrate", "suspensorium"),
]

# Motion verbs, as stems so "flex", "flexes", "flexion" all match.
MOTION = [
    ("flex", "flexion"), ("extend", "extension"), ("extens", "extension"),
    ("abduct", "abduction"), ("adduct", "adduction"),
    ("protract", "protraction"), ("retract", "retraction"),
    ("elevat", "elevation"), ("lift", "elevation"), ("rais", "elevation"),
    ("depress", "depression"), ("lower", "depression"),
    ("supinat", "supination"), ("pronat", "pronation"),
    ("invert", "inversion"), ("evert", "eversion"),
    ("stabilis", "stabilisation"), ("stabiliz", "stabilisation"),
    ("open", "opening"), ("clos", "closing"),
    ("dorsiflex", "flexion"), ("plantarflex", "extension"),
]

# Rotation needs its direction, so it is handled apart from the stem list.
ROTATION = [("medially rotat", "rotation-medial"), ("laterally rotat", "rotation-lateral"),
            ("medial rotat", "rotation-medial"), ("lateral rotat", "rotation-lateral"),
            ("internally rotat", "rotation-medial"), ("externally rotat", "rotation-lateral")]

# Whole phrases that name a motion and a joint together, checked before clauses.
DIRECT = [
    ("closes the jaw", ("jaw-joint", "closing")),
    ("adducts the mandible", ("jaw-joint", "closing")),
    ("opens the jaw", ("jaw-joint", "opening")),
    ("depresses the mandible", ("jaw-joint", "opening")),
    ("supinates the forearm", ("radioulnar", "supination")),
    ("pronates the forearm", ("radioulnar", "pronation")),
    ("supinates the antebrachium", ("radioulnar", "supination")),
    ("pronates the antebrachium", ("radioulnar", "pronation")),
    ("lateral bending", ("intervertebral", "lateral-bending")),
    ("lateral undulation", ("intervertebral", "lateral-bending")),
]

# Cues whose joint depends on which appendage the record belongs to. "Adducts
# the toes" and "flexes the digits" name the same joint class in either limb,
# and only the record's own region says which.
APPENDAGE = {
    "pectoral": "fore", "arm": "fore", "forearm": "fore", "hand": "fore",
    "pelvic": "hind", "thigh": "hind", "leg": "hind", "foot": "hind",
}
LIMB_CUES = {
    "fore": [("digit", "metacarpophalangeal"), ("finger", "metacarpophalangeal"),
             ("limb", "shoulder")],
    "hind": [("toe", "metatarsophalangeal"), ("digit", "metatarsophalangeal"),
             ("limb", "hip")],
}

# Motions that name their own joint. "May assist pronation and supination" has
# no segment in the clause, so it would otherwise inherit whatever the previous
# clause moved — which put the anconeus's rotational role at the elbow, where
# no rotation happens. Applied before inheritance, and only when the clause
# names no segment of its own.
MOTION_DEFAULT = {
    "fore": {"pronation": "radioulnar", "supination": "radioulnar"},
    "hind": {"pronation": "ankle", "supination": "ankle",
             "inversion": "ankle", "eversion": "ankle"},
}

# The parses that need a human. Each replaces the whole row set for that
# (muscle, scope), and each is here because the sentence names two structures
# and only one of them is the thing being moved.
OVERRIDE = {
    # "the scapular head also retracts the humerus" — the humerus moves, at the
    # shoulder; the scapula is only saying which head does it.
    ("triceps-brachii", "consensus"): [
        {"joint": "elbow", "motion": "extension"},
        {"joint": "shoulder", "motion": "retraction"},
    ],
    # "stabilises the two long bones of the crus against one another" is the
    # joint BETWEEN them, not the one above them.
    ("interosseus-cruris", "consensus"): [
        {"joint": "tibiofibular", "motion": "stabilisation"},
    ],
    # "assists ... in limb retraction and flexes the tail laterally" — two
    # joints, and the tail clause must not capture the limb one.
    ("caudalipuboischiotibialis", "consensus"): [
        {"joint": "hip", "motion": "retraction"},
        {"joint": "intervertebral", "motion": "lateral-bending"},
    ],
}

CLAUSE = re.compile(r"[;,.]| and | but | while | then ")

# "the long head also extends the arm" is about a head OF A MUSCLE, and reading
# the cranium out of it put triceps extension at the craniovertebral joint.
# Neutralised before parsing rather than guarded with a lookbehind, because the
# list of qualifiers is open and the failure is silent.
MUSCLE_HEAD = re.compile(
    r"\b(long|short|lateral|medial|deep|superficial|scapular|humeral|"
    r"clavicular|sternal|coracoid|ulnar|radial|oblique|straight)\s+heads?\b")


def resolve(text, region=None):
    """-> (rows, unclaimed clause fragments)."""
    low = MUSCLE_HEAD.sub("part", text.lower())
    rows, seen = [], set()

    def add(joint, motion):
        if (joint, motion) not in seen:
            seen.add((joint, motion))
            rows.append({"joint": joint, "motion": motion})

    for phrase, (joint, motion) in DIRECT:
        if phrase in low:
            add(joint, motion)
            low = low.replace(phrase, " ")

    parsed = []
    for clause in CLAUSE.split(low):
        clause = clause.strip()
        if not clause:
            continue

        motions = [m for stem, m in ROTATION if stem in clause]
        if not motions:
            motions = [m for stem, m in MOTION if stem in clause]

        # Rotational motions name their own joint and OUTRANK any segment in
        # the clause: the forearm pronates at the radioulnar joint whatever
        # noun the sentence uses, so "extends the wrist and assists supination"
        # must not land supination at the wrist, and the anconeus's rotational
        # role must not land at the elbow, where no rotation happens.
        defaults = MOTION_DEFAULT.get(APPENDAGE.get(region), {})
        joint = next((defaults[m] for m in motions if m in defaults), None)

        # Then appendage-specific cues: "adducts the toes toward the foot's
        # axis" is a metatarsophalangeal action, and reading "foot" out of it
        # would put it at the ankle. Closed on both sides, because the
        # "digitations" of the serratus are not digits.
        if not joint:
            for seg, j in LIMB_CUES.get(APPENDAGE.get(region), []):
                if re.search(r"\b" + re.escape(seg) + r"s?\b", clause):
                    joint = j
                    break
        # Then longest segment name first, so "pectoral girdle" is not read as
        # "girdle" and "hindlimb" is not read as "limb".
        if not joint:
            for seg, j in sorted(SEGMENT_JOINT, key=lambda x: -len(x[0])):
                if re.search(r"\b" + re.escape(seg), clause):
                    joint = j
                    break

        # Kept even with no motion: "protracts, retracts and rotates the
        # scapula" puts the segment in the one clause whose verb the vocabulary
        # does not cover, because a bare "rotates" has no direction and should
        # not become a motion. Dropping that clause stranded the other two.
        parsed.append({"clause": clause, "motions": motions, "joint": joint})

    # English coordination drops the shared object: "adducts and retracts the
    # humerus" splits into a clause with a verb and no segment, and one with
    # both. Let a verb-only clause take the segment from its nearest neighbour
    # that has one — forwards first, since the object usually trails the verbs.
    unclaimed = []
    for i, p in enumerate(parsed):
        if p["joint"]:
            continue
        nxt = next((q["joint"] for q in parsed[i + 1:] if q["joint"]), None)
        prv = next((q["joint"] for q in reversed(parsed[:i]) if q["joint"]), None)
        p["joint"] = nxt or prv

    for p in parsed:
        if not p["motions"]:
            continue                      # a joint-only clause; nothing to assert
        if not p["joint"]:
            unclaimed.append(p["clause"][:60])
            continue
        for m in dict.fromkeys(p["motions"]):
            add(p["joint"], m)

    return rows, unclaimed


def main():
    write = "--write" in sys.argv
    jdoc = json.loads(JOINTS.read_text())
    joints = {j["id"]: j for j in jdoc["joints"]}
    motions = set(jdoc["motions"])

    for _, (j, m) in DIRECT:
        if j not in joints or m not in motions:
            sys.exit(f"seed error: DIRECT rule targets unknown {j}/{m}")
    for _, j in SEGMENT_JOINT:
        if j not in joints:
            sys.exit(f"seed error: SEGMENT_JOINT targets unknown joint '{j}'")

    skel = json.loads((ROOT / "data" / "skeleton.json").read_text())
    graph = jointgraph.build(jdoc, {e["id"]: e for e in skel["elements"]})

    docs = {p: json.loads(p.read_text()) for p in MUSCLE_FILES}
    applied = unchanged = 0
    skipped = []
    corrected = []
    mismatched = []

    for path, doc in docs.items():
        for m in doc["muscles"]:
            spans = graph.spanned_by(m.get("attachments"))
            holders = [(m, (m.get("consensus") or {}).get("action"), "consensus")]
            for o in m.get("occurrences", []):
                holders.append((o, o.get("action"), o["taxon"]))
            for holder, text, tag in holders:
                if not text:
                    continue
                rows, unclaimed = resolve(text, m.get("region"))
                if unclaimed:
                    skipped.append(f"{m['id']}/{tag}: {' | '.join(unclaimed)}")

                if (m["id"], tag) in OVERRIDE:
                    rows = [dict(r) for r in OVERRIDE[(m["id"], tag)]]
                    corrected.append(f"{m['id']}/{tag}: curated override")

                # The graph checks the parse; it does not overrule it. An
                # earlier version reassigned any row naming an unspanned joint
                # to the single spanned joint permitting that motion. It fixed
                # the triceps and broke the contrahentium caput longum, which
                # inserts on the carpals and acts on the digits THROUGH the
                # contrahentes tendons — as the flexor accessorii do through
                # `flexor-tendons`. A muscle acting via another's tendon spans
                # nothing the graph can see, so an automatic correction there
                # replaces a right answer with a confident wrong one. Mismatches
                # are reported instead, and the handful the parser genuinely
                # gets wrong are curated in OVERRIDE above.
                for row in rows:
                    if not spans or row["joint"] in spans or row["joint"] in graph.exempt:
                        continue
                    mismatched.append(
                        f"{m['id']}/{tag}: {row['motion']} at {row['joint']}, "
                        f"which it does not span ({', '.join(sorted(spans))})")
                rows = [dict(t) for t in {tuple(sorted(r.items())) for r in rows}]
                rows.sort(key=lambda r: (r["joint"], r["motion"]))
                if not rows:
                    continue
                if holder.get("actions") == rows:
                    unchanged += 1
                    continue
                applied += 1
                if write:
                    holder["actions"] = rows

    for line in sorted(corrected):
        print(f"  OVERRIDE     {line}")
    for line in sorted(mismatched):
        print(f"  UNSPANNED    {line}")
    for line in sorted(skipped):
        print(f"  NOT CLAIMED  {line}")

    print(f"\n{applied} rows to apply, {unchanged} already current, "
          f"{len(skipped)} clauses left to the prose")

    if write and applied:
        for path, doc in docs.items():
            path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        print(f"wrote {len(docs)} files")
    elif not write:
        print("(dry run — pass --write to apply)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
