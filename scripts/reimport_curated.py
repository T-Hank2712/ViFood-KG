"""Clear Neo4j and import every curated release currently present."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase
import yaml

from food_kg.graph import Neo4jImporter
from food_kg.models import NodeRecord, RelationshipRecord
from food_kg.services.quality_gate import validate_release_gate


ROOT = Path(__file__).parents[1]


def read_json(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def clear_database(uri: str, user: str, password: str, database: str) -> int:
    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        with driver.session(database=database) as session:
            return session.run(
                """
                MATCH (n)
                WITH collect(n) AS nodes, count(n) AS node_count
                FOREACH (node IN nodes | DETACH DELETE node)
                RETURN node_count
                """
            ).single()["node_count"]
    finally:
        driver.close()


def release_paths(manifest: Path) -> tuple[Path, Path, Path]:
    release_name = manifest.name.removesuffix(".attested.yaml")
    return (
        ROOT / "data/curated/nodes" / f"{release_name}.json",
        ROOT / "data/curated/relationships" / f"{release_name}.json",
        manifest,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Clear Neo4j and import all curated releases")
    parser.add_argument("--clear", action="store_true", help="Delete all existing graph data before import")
    parser.add_argument("--yes", action="store_true", help="Required with --clear")
    args = parser.parse_args()
    if args.clear and not args.yes:
        raise SystemExit("Refusing to clear Neo4j without --yes")

    load_dotenv()
    uri = os.environ["NEO4J_URI"]
    user = os.environ["NEO4J_USER"]
    password = os.environ["NEO4J_PASSWORD"]
    database = os.getenv("NEO4J_DATABASE", "neo4j")

    if args.clear:
        deleted = clear_database(uri, user, password, database)
        print(f"Deleted {deleted} nodes from {database}.")

    registry = yaml.safe_load((ROOT / "config/source_registry.yaml").read_text(encoding="utf-8"))
    policy = yaml.safe_load((ROOT / "config/quality_gate.yaml").read_text(encoding="utf-8"))
    importer = Neo4jImporter.from_environment(uri, user, password, database)
    try:
        for manifest_path in sorted((ROOT / "data/curated/releases").glob("*.attested.yaml")):
            nodes_path, relationships_path, _ = release_paths(manifest_path)
            nodes = [NodeRecord.model_validate(item) for item in read_json(nodes_path)]
            relationships = [RelationshipRecord.model_validate(item) for item in read_json(relationships_path)]
            manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
            errors = validate_release_gate(nodes, relationships, manifest, registry, policy, ROOT)
            if errors:
                raise ValueError(f"{manifest_path.name} failed quality gate:\n- " + "\n- ".join(errors))
            stats = importer.import_release(nodes, relationships)
            print(f"{manifest['version']}: merged {stats.nodes_merged} nodes and {stats.relationships_merged} relationships.")
    finally:
        importer.close()


if __name__ == "__main__":
    main()
