# Tasks: Canonical KG Pipeline

## Phase 1: Contract Documentation

- [ ] T001 Document canonical pipeline boundary in `docs/contracts/kg-builder-contract.md`
- [ ] T002 Add machine-readable schema contract in `data/contracts/kg_schema_contract.json`
- [ ] T003 Ensure contract references current nutrient/additive release IDs

## Phase 2: Validation

- [ ] T004 Add tests that contract entity labels exist in ontology
- [ ] T005 Add tests that contract match keys exist in curated samples
- [ ] T006 Add compatibility check notes for ViFood-KG-Builder

## Phase 3: Verification

- [ ] T007 Run `PYTHONPATH=src .venv/bin/python -m pytest -q`
- [ ] T008 Confirm no curated release files were modified for contract-only changes
