"""Clear all data from the configured Neo4j database."""

from __future__ import annotations

import argparse
import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


def main() -> None:
    parser = argparse.ArgumentParser(description="Delete all nodes and relationships from Neo4j")
    parser.add_argument("--yes", action="store_true", help="Required confirmation for destructive cleanup")
    args = parser.parse_args()
    if not args.yes:
        raise SystemExit("Refusing to clear Neo4j without --yes")

    load_dotenv()
    driver = GraphDatabase.driver(os.environ["NEO4J_URI"], auth=(os.environ["NEO4J_USER"], os.environ["NEO4J_PASSWORD"]))
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    try:
        with driver.session(database=database) as session:
            deleted = session.run(
                """
                MATCH (n)
                WITH collect(n) AS nodes, count(n) AS node_count
                FOREACH (node IN nodes | DETACH DELETE node)
                RETURN node_count
                """
            ).single()["node_count"]
            print(f"Deleted {deleted} nodes from {database}.")
    finally:
        driver.close()


if __name__ == "__main__":
    main()
