"""Validation for the public contract consumed by ViFood-KG-Builder."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from food_kg.models import NODE_LABELS


CATALOG_ENTITY_TYPES = ("nutrient", "additive")
REQUIRED_TOP_LEVEL_FIELDS = {
    "contract_version",
    "producer_project",
    "consumer_project",
    "release_contracts",
    "supported_entities",
    "provenance_rules",
}


def load_builder_contract(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_builder_contract(contract: dict[str, Any], project_root: Path) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_TOP_LEVEL_FIELDS - set(contract)
    if missing:
        errors.append(f"Contract missing required fields: {sorted(missing)}")

    if contract.get("producer_project") != "ViFood-KG":
        errors.append("Contract producer_project must be ViFood-KG")
    if contract.get("consumer_project") != "ViFood-KG-Builder":
        errors.append("Contract consumer_project must be ViFood-KG-Builder")

    supported_entities = contract.get("supported_entities", {})
    if not isinstance(supported_entities, dict):
        return [*errors, "supported_entities must be an object"]

    for entity_type in CATALOG_ENTITY_TYPES:
        entity_contract = supported_entities.get(entity_type)
        if not isinstance(entity_contract, dict):
            errors.append(f"Missing supported entity contract: {entity_type}")
            continue
        label = entity_contract.get("label")
        if label not in NODE_LABELS:
            errors.append(f"{entity_type}: unsupported canonical label {label!r}")
        if entity_contract.get("canonical_status") != "catalog_first":
            errors.append(f"{entity_type}: canonical_status must be catalog_first")
        if not entity_contract.get("match_keys"):
            errors.append(f"{entity_type}: match_keys must not be empty")

    ingredient_contract = supported_entities.get("ingredient")
    if not isinstance(ingredient_contract, dict):
        errors.append("Missing supported entity contract: ingredient")
    else:
        if ingredient_contract.get("canonical_status") != "outside_vifood_kg_canonical_scope":
            errors.append("ingredient: canonical_status must be outside_vifood_kg_canonical_scope")
        if "catalog" in str(ingredient_contract.get("runtime_create_policy", "")).casefold():
            errors.append("ingredient: runtime_create_policy must not require a ViFood-KG catalog")

    release_contracts = contract.get("release_contracts", {})
    if not isinstance(release_contracts, dict):
        return [*errors, "release_contracts must be an object"]

    for release_key in ("nutrient", "additive"):
        release_id = release_contracts.get(release_key)
        if not release_id:
            errors.append(f"release_contracts.{release_key} is required")
            continue
        nodes_path = project_root / "data" / "curated" / "nodes" / f"{release_id}.json"
        relationships_path = project_root / "data" / "curated" / "relationships" / f"{release_id}.json"
        if not nodes_path.is_file():
            errors.append(f"{release_key}: nodes release is missing: {nodes_path.relative_to(project_root)}")
        if not relationships_path.is_file():
            errors.append(f"{release_key}: relationships release is missing: {relationships_path.relative_to(project_root)}")

    if not errors:
        errors.extend(_validate_match_key_samples(contract, project_root))
    return errors


def _validate_match_key_samples(contract: dict[str, Any], project_root: Path) -> list[str]:
    release_contracts = contract["release_contracts"]
    checks = {
        "nutrient": {
            "label": "Nutrient",
            "release": release_contracts["nutrient"],
            "properties": ("external_code", "name", "name_vi"),
        },
        "additive": {
            "label": "Additive",
            "release": release_contracts["additive"],
            "properties": ("ins", "name", "name_vi"),
        },
    }
    errors: list[str] = []
    for entity_type, check in checks.items():
        nodes_path = project_root / "data" / "curated" / "nodes" / f"{check['release']}.json"
        nodes = json.loads(nodes_path.read_text(encoding="utf-8"))
        entity_nodes = [node for node in nodes if node.get("label") == check["label"]]
        if not entity_nodes:
            errors.append(f"{entity_type}: release contains no {check['label']} nodes")
            continue
        for property_name in check["properties"]:
            if not any(node.get("properties", {}).get(property_name) for node in entity_nodes):
                errors.append(f"{entity_type}: no sample node has match property {property_name}")
    return errors
