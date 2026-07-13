# Implementation Plan: KG Builder Contract

**Branch**: `002-kg-builder-contract` | **Date**: 2026-07-13 | **Spec**: [spec.md](./spec.md)

## Summary

Tạo contract chính thức để ViFood-KG-Builder match/write theo schema của ViFood-KG mà không trộn code hay làm mất vai trò canonical/runtime.

## Technical Context

**Format**: Markdown + JSON

**Validation**: pytest or JSON schema in future

## Project Structure

```text
docs/contracts/kg-builder-contract.md
data/contracts/kg_schema_contract.json
specs/002-kg-builder-contract/
```

## Phase 0: Research

Đã chốt contract versioned data.

## Phase 1: Design

Contract includes Nutrient/Additive/Ingredient match policy.
