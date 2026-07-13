"""Semantic validation applied before a curated release reaches Neo4j."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Iterable

from food_kg.models import NodeRecord, RelationshipRecord

REQUIRED_PROVENANCE = {"reviewed_at"}
RELATION_ENDPOINTS = {
    "HAS_FUNCTION": {("Additive", "FunctionalClass")}, "PERMITTED_IN": {("Additive", "FoodCategory")},
    "COMMON_IN": {("Additive", "FoodCategory")}, "OBSERVED_IN": {("Additive", "FoodCategory")},
    "REFERS_TO": {("Alias", "Nutrient"), ("Alias", "Additive"), ("Alias", "FoodCategory"), ("Alias", "Allergen")},
    "SUBJECT_OF": {("HealthClaim", "Nutrient"), ("HealthClaim", "Additive")},
    "OUTCOME": {("HealthClaim", "HealthOutcome")}, "EVIDENCED_BY": {("HealthClaim", "Source")},
    "GOVERNS": {("Regulation", "Additive")},
    "BROADER_THAN": {("FoodCategory", "FoodCategory")},
    "SUPPORTED_BY": {
        ("Alias", "Source"), ("Allergen", "Source"), ("Additive", "Source"),
        ("FoodCategory", "Source"), ("FunctionalClass", "Source"),
        ("HealthOutcome", "Source"), ("Nutrient", "Source"), ("Regulation", "Source"),
    },
    "SUPERSEDES": {("Regulation", "Regulation")},
}

def validate_curated_graph(nodes: Iterable[NodeRecord], relationships: Iterable[RelationshipRecord]) -> list[str]:
    nodes, relationships = list(nodes), list(relationships)
    errors: list[str] = []
    ids = [node.id for node in nodes]
    duplicate_ids = [item for item, count in Counter(ids).items() if count > 1]
    errors.extend(f"Duplicate node id: {node_id}" for node_id in duplicate_ids)
    labels = {node.id: node.label for node in nodes}
    for node in nodes:
        missing = REQUIRED_PROVENANCE - node.properties.keys()
        if missing:
            errors.append(f"{node.id}: missing provenance {sorted(missing)}")
    relation_count = defaultdict(int)
    for rel in relationships:
        start_label, end_label = labels.get(rel.start_id), labels.get(rel.end_id)
        if not start_label or not end_label:
            errors.append(f"{rel.type}: endpoint must exist in this release ({rel.start_id} -> {rel.end_id})")
            continue
        allowed = RELATION_ENDPOINTS[rel.type]
        if allowed and (start_label, end_label) not in allowed:
            errors.append(f"{rel.type}: invalid endpoints {start_label} -> {end_label}")
        relation_count[(rel.start_id, rel.type)] += 1
    for claim in (node for node in nodes if node.label == "HealthClaim"):
        for relation in ("SUBJECT_OF", "OUTCOME", "EVIDENCED_BY"):
            if not relation_count[(claim.id, relation)]:
                errors.append(f"{claim.id}: missing required {relation}")
        for field in ("claim_text", "conditions_of_use", "evidence_level", "reviewed_at"):
            if not claim.properties.get(field):
                errors.append(f"{claim.id}: missing health-claim field {field}")
    return errors
