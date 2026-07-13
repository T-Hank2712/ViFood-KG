# Implementation Plan: Canonical KG Pipeline

**Branch**: `001-canonical-kg-pipeline` | **Date**: 2026-07-13 | **Spec**: [spec.md](./spec.md)

## Summary

Giữ ViFood-KG là canonical knowledge core. Không trộn runtime AI flow vào curated pipeline. Công bố Builder contract để ViFood-KG-Builder match/write theo schema chuẩn.

## Technical Context

**Language/Version**: Python 3.x

**Primary Dependencies**: pydantic, PyYAML, Neo4j driver, pytest

**Storage**: curated JSON/YAML files and Neo4j

**Testing**: pytest fixtures for release validation and importer idempotency

## Constitution Check

- Reproducible Data Pipelines: PASS
- Source Traceability: PASS
- Schema Consistency: PASS
- Testable Graph Behavior: PASS
- Minimal, Observable Integrations: PASS

## Project Structure

```text
config/source_registry.yaml
data/curated/
docs/contracts/
data/contracts/
src/food_kg/
specs/001-canonical-kg-pipeline/
```

## Phase 0: Research

Đã chốt canonical pipeline và Builder contract boundary.

## Phase 1: Design

Artifacts: `data-model.md`, `quickstart.md`, `tasks.md`, contract docs.
