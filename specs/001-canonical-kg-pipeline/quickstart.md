# Quickstart: Canonical KG Pipeline

## Validate Current Releases

```bash
PYTHONPATH=src .venv/bin/python -m pytest -q
```

## Import Curated Data

```bash
PYTHONPATH=src .venv/bin/python scripts/reimport_curated.py --clear --yes
```

## Contract Files

Builder-facing contract lives at:

```text
docs/contracts/kg-builder-contract.md
data/contracts/kg_schema_contract.json
```

ViFood-KG-Builder should consume these as schema/matching reference, not as runtime code.
