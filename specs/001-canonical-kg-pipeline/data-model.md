# Data Model: Canonical KG Pipeline

## Curated Release Shape

```text
data/curated/nodes/<release>.json
data/curated/relationships/<release>.json
data/curated/releases/<release>.attested.yaml
```

## NodeRecord

| Field | Required | Type | Notes |
| --- | --- | --- | --- |
| `label` | Yes | string | Một trong ontology labels |
| `id` | Yes | string | Stable ID, uppercase namespace |
| `properties` | Yes | object | JSON-serializable properties |

## RelationshipRecord

| Field | Required | Type | Notes |
| --- | --- | --- | --- |
| `start_id` | Yes | string | Existing node ID |
| `end_id` | Yes | string | Existing node ID |
| `type` | Yes | string | Ontology relationship type |
| `properties` | Yes | object | Relationship metadata |

## Canonical Requirements

- Business nodes must be supported by `Source`.
- `Alias` must use `REFERS_TO`.
- `HealthClaim` evidence must use `EVIDENCED_BY`.
- Do not duplicate `source_url` on business nodes when `Source.url` exists.

## Builder Contract Output

ViFood-KG must publish a contract for Builder:

```text
docs/contracts/kg-builder-contract.md
data/contracts/kg_schema_contract.json
```
