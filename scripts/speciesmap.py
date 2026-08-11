"""Species -> clade, for the scripts that still think in operational taxa.

Occurrences are keyed on species and the clade is derived; nothing stores it.
Every script that used to read `occ["taxon"]` calls `clade_of(occ)` instead, so
there is exactly one place that knows how the derivation works.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _load():
    with open(ROOT / "data/species.json") as fh:
        return {s["id"]: s for s in json.load(fh)["species"]}


SPECIES = _load()
CLADE = {sid: s.get("clade") for sid, s in SPECIES.items()}
BINOMIAL = {sid: s.get("binomial", sid) for sid, s in SPECIES.items()}


def clade_of(occ):
    """The operational taxon an occurrence rolls up into.

    Falls back to a literal `taxon` key. Nothing in `data/` carries one any
    more, but seed scripts build occurrence dicts in memory before they are
    attributed, and a seed whose idempotency check silently returns None appends
    a duplicate row on every run.
    """
    sid = occ.get("species")
    if sid in CLADE:
        return CLADE[sid]
    return occ.get("taxon")


def species_of(occ):
    return occ.get("species")
