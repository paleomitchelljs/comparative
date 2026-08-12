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
    # UNRESOLVED — see docs/GAPS.md §7. Dick & Clemente name no *V. exanthematicus*:
    # their own dissections are nine other varanids, and the Table 1 the attachment
    # rows come from is a compilation "of the varanid hindlimb" from Snyder (1954),
    # Gans et al., Reilly (Sceloporus clarki) and Anzai et al. (Anolis) — two of the
    # four not varanids at all. The species was borrowed from Cieri's monitor. Left
    # in place only because removing it hands the rows to Diogo & Molnar's Timon,
    # which is a different animal nobody observed these attachments in.
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
    "schreiweis-1982": "eudyptes-pachyrhynchus",
    "widrig-etal-2023": "nothoprocta-pentlandii",
    "fisher-goodman-1955": "grus-americana",
    "mckitrick-1991": "gavia-immer",
    "boumans-etal-2015": "tyto-furcata",
    "jones-etal-2019": "columba-livia",
    "springer-johnson-2015": "protanguilla-palau",
    # naumann-etal-2017 is two species, not one — see SURVEY_EXEMPLARS.
    "omura-etal-2014": "necturus-maculosus",
    "bauer-1997": "necturus-maculosus",
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
    # Not Felis catus, which appears twice as a comparison: the animals are a jaguar,
    # an ocelot and a Geoffroy's cat, and each row names its own in prose.
    "sanchez-etal-2019": "panthera-onca",
    # Gyambibi & Lemelin dissected 17 prosimians across eleven genera — Propithecus,
    # Varecia, Nycticebus, Otolemur, Microcebus and more — and Lemelin & Diogo is a
    # review across the whole order. Neither examines a human; both were mapped to
    # Homo sapiens, which would have attributed a lemur's forearm to a person the
    # moment either was mined. Rows will name their own animal in prose instead.
}

# --- multi-taxon surveys: the exemplar each names for each clade ------------
SURVEY_EXEMPLARS = {
    "abdala-diogo-2010": {
        "caudata": "ambystoma-ordinarium", "anura": "rhinella-arenarum",
        "testudines": "trachemys-scripta", "lepidosauria": "timon-lepidus",
        "crocodylia": "caiman-latirostris", "aves": "gallus-domesticus",
        # Tables 2 and 3 add "the mammal Rattus" to the six reptile and amphibian
        # columns. Five hand and pectoral rows had been guessed onto a cheetah.
        "theria": "rattus-norvegicus",
    },
    # NOT Abdala & Diogo's six-column set, which was copied here wholesale. This is
    # the hindlimb companion and its Materials names FOUR key taxa: "the salamander
    # Ambystoma mexicanum, the lizard Timon lepidus, the rodent Rattus norvegicus,
    # and modern humans". Caiman and Rhinella appear zero times in the paper,
    # Ornithorhynchus once and Gallus twice, all as literature. Its anuran, chelonian,
    # crocodylian, avian and monotreme statements are review, so they get no exemplar.
    "diogo-molnar-2014": {
        "caudata": "ambystoma-mexicanum", "lepidosauria": "timon-lepidus",
        "theria": "rattus-norvegicus",
    },
    # Their five clade representatives are stated outright: "chondrichthyans (shark
    # Squalus) ... actinopterygians (bichir Polypterus) ... coelacanths (Latimeria)
    # ... dipnoans (Neoceratodus); and tetrapods (Ambystoma)". The salamander is
    # A. mexicanum — carried over from their own earlier axolotl work, not the
    # A. ordinarium of the forelimb paper. Squalus is genus-only in the text.
    "diogo-etal-2016": {
        "chondrichthyes": "squalus-acanthias", "actinopterygii": "polypterus-senegalus",
        "actinistia": "latimeria-chalumnae", "dipnoi": "neoceratodus-forsteri",
        "caudata": "ambystoma-mexicanum",
    },
    "diogo-etal-2016-si": {
        "chondrichthyes": "squalus-acanthias", "actinopterygii": "polypterus-senegalus",
        "actinistia": "latimeria-chalumnae", "dipnoi": "neoceratodus-forsteri",
        "caudata": "ambystoma-mexicanum",
    },
    # Their hagfish is Myxine glutinosa (2 juveniles, dissected). Eptatretus appears
    # only as other people's developmental work. The selachian is stated: "our
    # descriptions of selachians are based on Squalus acanthias, and not on Mustelus".
    "ziermann-etal-2014": {
        "myxini": "myxine-glutinosa", "petromyzontida": "petromyzon-marinus",
        "chondrichthyes": "squalus-acanthias",
    },
    # Dissected, and listed with specimen counts: "squamates Iguana iguana [2] and
    # Varanus indicus [1], turtle Chelydra serpentina [1], crocodilians Paleosuchus
    # palpebrosus [1] and Crocodylus porosus [2], and avians Gallus gallus [1] and
    # Grus japonensis [1]". Timon, Trachemys and Caiman appear nowhere in the paper —
    # three more of Abdala & Diogo's exemplars borrowed for a study that used none.
    "hattori-tsuihiji-2021": {
        "lepidosauria": "iguana-iguana", "testudines": "chelydra-serpentina",
        "crocodylia": "crocodylus-porosus", "aves": "gallus-domesticus",
    },
    "allen-etal-2021": {"aves": "gallus-domesticus", "crocodylia": "alligator-mississippiensis"},
    "fahn-lai-etal-2020": {"monotremata": "tachyglossus-aculeatus", "theria": "monodelphis-domestica"},
    "werneburg-2011": {"testudines": "trachemys-scripta"},
    # NOT Trachemys, which the paper never mentions. Werneburg & Maier's series are
    # the cryptodire Chrysemys picta and the pleurodire Emydura subglobosa; Chrysemys
    # is the emydid, so it stands where the turtle column already sits.
    "werneburg-maier-2019": {"testudines": "chrysemys-picta"},
    # NOT Timon, which appears nowhere in Johnston 2014. The lizard he figures is
    # Ctenosaura pectinata — "chosen" for the missing ventral temporal arch — and his
    # plesiomorphic reference is Sphenodon. Borrowed from Abdala & Diogo, like the
    # Rhinella that was taken off Sigurdsen et al.
    "johnston-2014": {"lepidosauria": "ctenosaura-pectinata"},
    # Navarro et al. work on South American lizards; Timon lepidus is European and was
    # borrowed from Abdala & Diogo. No local PDF to name the animal from, so the rows
    # must carry their own species in prose — as the two that cite it already do.
    # NOT Rhinella: Sigurdsen et al. examine no bufonid but Anaxyrus americanus, and
    # their dissected and figured frogs are Leiopelma and Ascaphus. The old mapping was
    # Abdala & Diogo's anuran exemplar borrowed for a paper that does not use it.
    "sigurdsen-etal-2012": {"anura": "leiopelma-hochstetteri"},
    # The gar is the study animal; the axolotl is the comparison it is read against.
    "naumann-etal-2017": {"actinopterygii": "lepisosteus-osseus",
                          "caudata": "ambystoma-mexicanum"},
    # Johnston dissected Leiopelma and Ascaphus and tested the folded-sheet model on
    # comparative material from chondrichthyans to mammals; the cartilaginous fish in
    # that material is Callorhinchus.
    "johnston-2011": {"chondrichthyes": "callorhinchus-milii"},
    # Ziermann & Diogo (2013) is the axolotl paper AND its anuran comparison. Their
    # 2019 review is Scyliorhinus, Polypterus and Danio — it examines no tetrapod, so
    # it gets no exemplars here however many tetrapod rows once cited it.
    "ziermann-diogo-2013": {"caudata": "ambystoma-mexicanum", "anura": "xenopus-laevis"},
    # Schilling (2011) deliberately has NO per-clade exemplar. It is a review whose
    # only species-level data are the figures — Myxine, Etmopterus, Ambystoma
    # tigrinum, Dipsosaurus, Microtus (Fig. 2) and Ambystoma maculatum, Dipsosaurus,
    # Canis (Fig. 3) — and its crocodylian, avian and actinopterygian statements are
    # cladogram synthesis with no animal behind them. Rows attributed to it name
    # their species in prose instead, which is rule 1 and carries the evidence.
    #
    # Leavey et al. (2024) is out for the same reason and by the same test: Rhinella
    # appears zero times in it. Their sample is thirty-odd frogs compared across
    # locomotor modes — Breviceps poweri, Phlyctimantis maculatus, Neobatrachus
    # pictus and the rest — and no one of them is the exemplar. A third borrowing of
    # Abdala & Diogo's anuran column.
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
