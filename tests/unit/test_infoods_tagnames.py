from food_kg.extractors.infoods_tagnames import parse_tagnames


def test_parses_tagname_record_and_preserves_provenance() -> None:
    raw = """<NA> sodium\n    Unit: mg\n    Synonyms: natrium\n    Comments: Example comment.\n    Tables: USDA 307\n\n<K> potassium\n    Unit: mg\n"""
    records = list(parse_tagnames(raw, "PART1.TXT", "2026-06-22"))
    assert records == [
        {
            "source_tagname": "NA", "source_name": "sodium", "default_unit": "mg",
            "synonyms_raw": "natrium", "comments": "Example comment.", "tables": "USDA 307",
            "source_id": "SOURCE:FAO_INFOODS_TAGNAMES",
            "source_url": "https://www.fao.org/infoods/infoods/standards-guidelines/food-component-identifiers-tagnames/en/",
            "raw_file": "PART1.TXT", "raw_record_number": 1, "retrieved_at": "2026-06-22",
        },
        {
            "source_tagname": "K", "source_name": "potassium", "default_unit": "mg",
            "synonyms_raw": None, "comments": None, "tables": None,
            "source_id": "SOURCE:FAO_INFOODS_TAGNAMES",
            "source_url": "https://www.fao.org/infoods/infoods/standards-guidelines/food-component-identifiers-tagnames/en/",
            "raw_file": "PART1.TXT", "raw_record_number": 2, "retrieved_at": "2026-06-22",
        },
    ]


def test_default_unit_keeps_only_the_primary_unit_token() -> None:
    raw = """<VITA> vitamin A
    Unit: mcg. The value for <VITA> may be expressed in international units instead of the default unit of micrograms.

<NA> sodium
    Unit: mg Note: If the value is expressed in millimoles, mmol must be explicitly stated with the secondary tagname <UNIT/>.
"""
    records = list(parse_tagnames(raw, "PART4.TXT", "2026-06-22"))
    assert [record["default_unit"] for record in records] == ["mcg", "mg"]


def test_nutrient_name_keeps_only_text_before_semicolon() -> None:
    raw = """<CHOCDF> carbohydrate, total; calculated by difference
    Unit: g
"""
    records = list(parse_tagnames(raw, "PART1.TXT", "2026-06-22"))
    assert records[0]["source_name"] == "carbohydrate, total"
