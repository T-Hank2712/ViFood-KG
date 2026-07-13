# ViFood-KG Builder Contract

**Contract Version**: `2026-07-13.1`

**Producer**: `ViFood-KG`

**Consumer**: `ViFood-KG-Builder`

## Purpose

This contract defines how `ViFood-KG-Builder` may match and write data against the canonical graph produced by `ViFood-KG`.

The boundary is strict:

```text
ViFood-KG
= canonical knowledge core
= curated releases, source registry, quality gate, Neo4j catalog

ViFood-KG-Builder
= runtime/orchestration layer
= AI extraction, entity matching, runtime create when allowed
```

Builder must not silently promote AI/runtime observations into curated knowledge. Missing or newly observed data must either be runtime-created with explicit provenance or sent back to a review/candidate flow.

## Global Graph Rules

- Business nodes use stable `id`.
- Provenance uses relationships to `Source`.
- Business nodes should not duplicate `source` or `source_url` properties when `Source.url` exists.
- Alias nodes use `(:Alias)-[:REFERS_TO]->(:Entity)`.
- Canonical releases are imported only after quality gate.

## Supported Entity Contracts

### Nutrient

**Canonical status**: catalog-first.

**Label**: `Nutrient`

**ID format**: `NUTRIENT:INFOODS_{TAGNAME}` for curated INFOODS nutrients.

**Required canonical properties**:

- `name`
- `external_code`
- `default_unit`
- `status`
- `reviewed_at`

**Optional common properties**:

- `name_vi`
- `vietnam_label_requirement`
- `source_version`

**Match keys for Builder**:

1. `external_code` / tagname when AI provides or Builder derives one.
2. Exact normalized `name_vi`.
3. Exact normalized `name`.
4. `Alias.name` through `(:Alias)-[:REFERS_TO]->(:Nutrient)`.

**Runtime create policy**:

Builder must match canonical catalog first. If no match exists, Builder may create a runtime Nutrient only through a nutrient-specific fallback with explicit provenance and stable ID. It must not alter curated release files.

### Additive

**Canonical status**: catalog-first.

**Label**: `Additive`

**ID format**: `ADDITIVE:INS_{NORMALIZED_INS}`

**Required canonical properties**:

- `name`
- `ins`
- `status`
- `reviewed_at`

**Optional common properties**:

- `name_vi`
- `raw_page_number`
- `raw_record_number`

**Match keys for Builder**:

1. Normalized `ins`.
2. E-number alias such as `E330`.
3. Exact normalized `name_vi`.
4. Exact normalized `name`.
5. `Alias.name` through `(:Alias)-[:REFERS_TO]->(:Additive)`.

**Runtime create policy**:

Builder must match canonical catalog first, prioritizing `ins`/E-code. If no match exists, Builder may create a runtime Additive only through additive-specific fallback with explicit provenance and stable ID. It must not alter curated release files.

### Ingredient

**Canonical status**: outside ViFood-KG canonical scope.

**Label**: `Ingredient`

**Runtime ID format**: `INGREDIENT:{WIKIDATA_QID}` when created from Wikidata.

**Builder policy**:

Builder owns Ingredient matching, Wikidata enrichment, and runtime creation. Builder should match existing `Ingredient` nodes in the target graph first. If no match exists, Builder may enrich from Wikidata and create a new Ingredient with provenance to `SOURCE:WIKIDATA`, following `ViFood-KG-Builder` feature `002-ingredient-wikidata-sync`.

**Runtime create policy**:

Ingredient is AI-first match-or-create in Builder. Do not expect ViFood-KG to provide an Ingredient catalog, Ingredient release, Ingredient extractor, or Wikidata Ingredient pipeline.

## Release Contracts

Current canonical releases Builder may match against:

| Entity | Release |
| --- | --- |
| Nutrient | `nutrients_vietnam_infoods_v0.2.0` |
| Additive | `vietnam_additive_master_v0.1.2` |
| Additive permissions | `vietnam_additive_permissions_2a_v0.1.0` |

## Compatibility Expectations

Builder should record the contract version and release IDs used for a workflow run:

```json
{
  "kg_contract_version": "2026-07-13.1",
  "matched_against_releases": {
    "nutrient": "nutrients_vietnam_infoods_v0.2.0",
    "additive": "vietnam_additive_master_v0.1.2"
  }
}
```

## Non-Goals

- This contract does not merge the two projects.
- This contract does not allow runtime AI output to bypass KG quality gate.
- This contract keeps Ingredient outside ViFood-KG canonical scope.
