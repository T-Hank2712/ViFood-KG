import copy
import json
from pathlib import Path

from food_kg.services.builder_contract import load_builder_contract, validate_builder_contract


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = PROJECT_ROOT / "data" / "contracts" / "kg_schema_contract.json"


def test_builder_contract_is_valid_against_curated_releases() -> None:
    contract = load_builder_contract(CONTRACT_PATH)

    assert validate_builder_contract(contract, PROJECT_ROOT) == []


def test_builder_contract_rejects_missing_release() -> None:
    contract = load_builder_contract(CONTRACT_PATH)
    invalid = copy.deepcopy(contract)
    invalid["release_contracts"]["nutrient"] = "missing_release"

    errors = validate_builder_contract(invalid, PROJECT_ROOT)

    assert any("nodes release is missing" in error for error in errors)


def test_builder_contract_keeps_ingredient_outside_kg_canonical_scope() -> None:
    contract = load_builder_contract(CONTRACT_PATH)

    ingredient = contract["supported_entities"]["ingredient"]

    assert ingredient["canonical_status"] == "outside_vifood_kg_canonical_scope"
    assert "catalog" not in ingredient["runtime_create_policy"].casefold()


def test_builder_contract_json_is_machine_readable() -> None:
    parsed = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    assert parsed["contract_version"]
    assert parsed["producer_project"] == "ViFood-KG"
    assert parsed["consumer_project"] == "ViFood-KG-Builder"
