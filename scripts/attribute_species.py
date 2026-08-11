#!/usr/bin/env python3
"""Assign a `species` to every muscle occurrence.

Occurrences used to be keyed on an operational taxon — a clade standing in for
whichever animal its source happened to dissect. That lost every disagreement
between species: Zaaf et al.'s two geckos insert the extensor carpi ulnaris on
DIFFERENT CARPALS, and under a single Lepidosauria row one of those observations
had to be demoted to prose. Species are the unit of observation; the clade is a
rollup computed from them.

Attribution runs in priority order, and each row records which rule fired so the
weak ones can be found again:

  note      the occurrence's own prose names a species. Strongest — it is what
            the person scoring the row was looking at.
  source    the row cites a single-species study.
  survey    the row cites a multi-taxon survey, and that survey names an
            exemplar for this clade (Abdala & Diogo dissected Timon lepidus for
            Lepidosauria, Caiman latirostris for Crocodylia, and so on).
  default   nothing better. Falls back to the clade's first exemplar, which is a
            guess and is flagged as one.

Idempotent: re-running overwrites `species` and `speciesBasis` from scratch.
"""
import json
import glob
import re
import sys
import collections

WRITE = "--write" in sys.argv

# --- single-species (or clearly primary-species) sources -------------------
SOURCE_SPECIES = {
    "walthall-ashley-ross-2006": "taricha-torosa",
    "ercoli-etal-2014": "galictis-cuja",
    "ercoli-etal-2012": "galictis-cuja",
    "klinkhamer-etal-2017": "crocodylus-porosus",
    "wiseman-etal-2021": "crocodylus-niloticus",
    "zaaf-etal-1999": "eublepharis-macularius",
    "meers-2003": "alligator-mississippiensis",
    "allen-etal-2014": "alligator-mississippiensis",
    "hutchinson-etal-2015": "struthio-camelus",
    "prikryl-etal-2009": "discoglossus-pictus",
    "johnston-2011": "ascaphus-truei",
    "dick-clemente-2016": "varanus-exanthematicus",
    "cieri-2018": "varanus-exanthematicus",
    "diogo-ziermann-2015": "squalus-acanthias",
    "godoy-etal-2016": "pissarrachampsa-sera",
    "liparini-schultz-2013": "prestosuchus-chiniquensis",
    "bodenham-etal-2026": "galahadosuchus-sp",
    "gambaryan-etal-2015": "tachyglossus-aculeatus",
    "molnar-etal-2018": "eusthenopteron-foordi",
    "winterbottom-1973": "teleostei-generalised",
    "jayaram-etal-1983": "arius-sp",
    "hudson-etal-2011a": "acinonyx-jubatus",
    "hudson-etal-2011b": "acinonyx-jubatus",
    "campbell-2007": "rattus-norvegicus",
    "ghetie-etal-1976": "gallus-domesticus",
    "matsuoka-hasegawa-2007": "cygnus-cygnus",
    "schreiweis-1982": "pygoscelis-sp",
    "widrig-etal-2023": "nothoprocta-pentlandii",
    "fisher-goodman-1955": "grus-americana",
    "mckitrick-1991": "gavia-sp",
    "boumans-etal-2015": "tyto-furcata",
    "naumann-etal-2017": "ambystoma-mexicanum",
    "omura-etal-2014": "necturus-maculosus",
    "molnar-etal-2017": "chamaeleo-calyptratus",
    "freitas-etal-2017": "iguana-iguana",
    "tomanska-etal-2024": "varanus-komodoensis",
    "tomanska-etal-2025": "varanus-komodoensis",
    "kepa-etal-2023": "varanus-komodoensis",
    "pereyra-etal-2024": "caiman-yacare",
    "blotto-etal-2020": "triprion-petasatus",
    "velez-garcia-etal-2023": "potos-flavus",
    "westphal-etal-2019": "amphisbaenia-generalised",
    "bishop-pierce-2024": "dimetrodon-sp",
    "sanchez-etal-2019": "felis-catus",
    "gyambibi-lemelin-2013": "homo-sapiens",
    "lemelin-diogo-2016": "homo-sapiens",
}

# --- multi-taxon surveys: the exemplar each names for each clade ------------
SURVEY_EXEMPLARS = {
    "abdala-diogo-2010": {
        "caudata": "ambystoma-ordinarium", "anura": "rhinella-arenarum",
        "testudines": "trachemys-scripta", "lepidosauria": "timon-lepidus",
        "crocodylia": "caiman-latirostris", "aves": "gallus-domesticus",
    },
    "diogo-molnar-2014": {
        "caudata": "ambystoma-ordinarium", "anura": "rhinella-arenarum",
        "testudines": "trachemys-scripta", "lepidosauria": "timon-lepidus",
        "crocodylia": "caiman-latirostris", "aves": "gallus-domesticus",
        "theria": "rattus-norvegicus", "monotremata": "ornithorhynchus-anatinus",
    },
    "diogo-etal-2016": {
        "chondrichthyes": "squalus-acanthias", "actinopterygii": "polypterus-senegalus",
        "actinistia": "latimeria-chalumnae", "dipnoi": "neoceratodus-forsteri",
        "caudata": "ambystoma-ordinarium",
    },
    "diogo-etal-2016-si": {
        "chondrichthyes": "squalus-acanthias", "actinopterygii": "polypterus-senegalus",
        "actinistia": "latimeria-chalumnae", "dipnoi": "neoceratodus-forsteri",
        "caudata": "ambystoma-ordinarium",
    },
    "ziermann-etal-2014": {
        "myxini": "eptatretus-burgeri", "petromyzontida": "petromyzon-marinus",
        "chondrichthyes": "squalus-acanthias",
    },
    "hattori-tsuihiji-2021": {
        "lepidosauria": "timon-lepidus", "testudines": "trachemys-scripta",
        "crocodylia": "caiman-latirostris", "aves": "gallus-domesticus",
    },
    "allen-etal-2021": {"aves": "gallus-domesticus", "crocodylia": "alligator-mississippiensis"},
    "fahn-lai-etal-2020": {"monotremata": "tachyglossus-aculeatus", "theria": "monodelphis-domestica"},
    "werneburg-2011": {"testudines": "trachemys-scripta"},
    "werneburg-maier-2019": {"testudines": "trachemys-scripta"},
    "johnston-2014": {"lepidosauria": "timon-lepidus"},
    "navarro-etal-2023": {"lepidosauria": "timon-lepidus"},
    "sigurdsen-etal-2012": {"anura": "rhinella-arenarum"},
    "leavey-etal-2024": {"anura": "rhinella-arenarum"},
}


def load():
    species = json.load(open("data/species.json"))["species"]
    by_id = {s["id"]: s for s in species}
    by_clade = collections.defaultdict(list)
    for s in species:
        by_clade[s["clade"]].append(s["id"])
    taxa = json.load(open("data/taxa.json"))["taxa"]
    return by_id, by_clade, {t["id"]: t for t in taxa}


def binomial_index(by_id):
    """Map every way a species might be written in prose onto its id."""
    idx = {}
    for sid, s in by_id.items():
        b = s["binomial"]
        idx[b] = sid
        parts = b.split()
        if len(parts) >= 2 and not parts[1].endswith("."):
            idx[f"{parts[0]} {parts[1]}"] = sid
    return idx


def attribute(occ, clade, idx, by_clade, by_id):
    # Every candidate must belong to the clade the row is about. A Chondrichthyes
    # row often cites an anuran paper for comparison; that is a citation, not an
    # observation of a shark, and taking its species would be a lie about who
    # looked at what.
    ok = lambda sid: sid and by_id.get(sid, {}).get("clade") == clade

    blob = " ".join(str(occ.get(k, "")) for k in
                    ("attachmentNote", "note", "divisionNote", "name"))

    # 1. the row's own prose names a species
    hits = sorted((blob.index(b), sid) for b, sid in idx.items() if b in blob)
    for _, sid in hits:
        if ok(sid):
            return sid, "note"

    srcs = occ.get("sources", []) or []

    # 2. a single-species source
    for k in srcs:
        sid = SOURCE_SPECIES.get(k)
        if ok(sid):
            return sid, "source"

    # 3. a survey that names an exemplar for this clade
    for k in srcs:
        sid = (SURVEY_EXEMPLARS.get(k) or {}).get(clade)
        if ok(sid):
            return sid, "survey"

    # 4. nothing better
    pool = by_clade.get(clade) or []
    return (pool[0] if pool else None), "default"


def main():
    by_id, by_clade, taxa = load()
    idx = binomial_index(by_id)
    basis = collections.Counter()
    unresolved = []

    for path in sorted(glob.glob("data/muscles-*.json")):
        doc = json.load(open(path))
        for m in doc["muscles"]:
            for occ in m.get("occurrences", []):
                # Re-running must be a no-op, so the clade context comes from
                # whatever the row already says: its species on a second pass,
                # its legacy `taxon` on the first.
                clade = (by_id.get(occ.get("species"), {}).get("clade")
                         or occ.get("taxon"))
                sid, how = attribute(occ, clade, idx, by_clade, by_id)
                if not sid:
                    unresolved.append(f"{m['id']}/{clade}")
                    continue
                if by_id[sid]["clade"] != clade:
                    unresolved.append(f"{m['id']}/{clade}: {sid} is not in that clade")
                    continue
                occ["species"] = sid
                occ["speciesBasis"] = how
                basis[how] += 1
        if WRITE:
            json.dump(doc, open(path, "w"), indent=2, ensure_ascii=False)
            open(path, "a").write("\n")

    total = sum(basis.values())
    print(f"attributed {total} occurrences" + ("" if WRITE else "  (dry run — pass --write)"))
    for k in ("note", "source", "survey", "default"):
        if basis[k]:
            print(f"  {k:8} {basis[k]:4}  ({basis[k]*100//total}%)")
    if unresolved:
        print(f"\nUNRESOLVED ({len(unresolved)}):")
        for u in unresolved[:20]:
            print("   ", u)


if __name__ == "__main__":
    main()
