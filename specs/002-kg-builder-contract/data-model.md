# Data Model: KG Builder Contract

## Contract

| Field | Required | Type |
| --- | --- | --- |
| `contract_version` | Yes | string |
| `producer_project` | Yes | string |
| `consumer_project` | Yes | string |
| `supported_entities` | Yes | object |
| `release_contracts` | Yes | object |
| `provenance_rules` | Yes | object |

## Entity Contract

| Field | Required | Type |
| --- | --- | --- |
| `label` | Yes | string |
| `id_format` | Yes | string |
| `required_properties` | Yes | list |
| `match_keys` | Yes | list |
| `relationships` | Yes | list |
| `runtime_create_policy` | Yes | string |
