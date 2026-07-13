# Feature Specification: KG Builder Contract

**Feature Branch**: `002-kg-builder-contract`

**Created**: 2026-07-13

**Status**: Draft

**Input**: "Định nghĩa contract dữ liệu giữa ViFood-KG và ViFood-KG-Builder. ViFood-KG công bố labels, relationships, ID formats, required properties, match keys và release IDs để Builder match Nutrient/Additive vào canonical graph và xử lý Ingredient theo rule riêng."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Builder match Nutrient theo contract (Priority: P1)

Builder cần biết `Nutrient` canonical match bằng `external_code`, `name`, `name_vi`, và `Alias`.

**Acceptance Scenarios**:

1. **Given** AI trả `Protein`, **When** Builder dùng contract, **Then** Builder biết phải match `Nutrient` bằng alias/name/tagname thay vì tạo mới ngay.
2. **Given** graph có `NUTRIENT:INFOODS_*`, **When** Builder match, **Then** Builder không tạo duplicate Nutrient.

---

### User Story 2 - Builder match Additive theo contract (Priority: P1)

Builder cần biết `Additive` canonical match bằng `ins`, E-code alias, `name`, `name_vi`, và `Alias`.

**Acceptance Scenarios**:

1. **Given** AI trả `INS 330` hoặc `E330`, **When** Builder dùng contract, **Then** Builder match vào `Additive` theo `ins` hoặc alias.
2. **Given** additive không match catalog, **When** Builder tạo mới, **Then** node mới phải có provenance riêng và không giả làm curated release.

---

### User Story 3 - Builder xử lý Ingredient ngoài catalog hiện tại (Priority: P1)

Ingredient chưa là catalog canonical do ViFood-KG import sẵn trong phase này, nên Builder match graph trước rồi mới Wikidata enrich/create.

**Acceptance Scenarios**:

1. **Given** graph đã có ingredient, **When** Builder nhận cùng ingredient từ AI, **Then** Builder dùng lại node.
2. **Given** graph chưa có ingredient, **When** Builder enrich Wikidata thành công, **Then** Builder tạo Ingredient với provenance `SOURCE:WIKIDATA`.

## Requirements *(mandatory)*

- **FR-001**: Contract PHẢI định nghĩa version.
- **FR-002**: Contract PHẢI định nghĩa supported entities `Nutrient`, `Additive`, `Ingredient`.
- **FR-003**: Contract PHẢI định nghĩa match keys cho `Nutrient`.
- **FR-004**: Contract PHẢI định nghĩa match keys cho `Additive`.
- **FR-005**: Contract PHẢI nói rõ `Ingredient` không có catalog canonical import nền trong phase này.
- **FR-006**: Contract PHẢI định nghĩa provenance rules.
- **FR-007**: Contract PHẢI liệt kê release IDs mà Builder có thể match against.

## Success Criteria *(mandatory)*

- **SC-001**: Builder có thể viết test match Nutrient từ contract mà không đọc source code ViFood-KG.
- **SC-002**: Builder có thể viết test match Additive từ contract mà không đọc source code ViFood-KG.
- **SC-003**: Contract không cho phép Builder tự động promote AI/runtime data thành curated KG release.

## Assumptions

- Builder và KG dùng cùng target Neo4j schema.
- Contract là dữ liệu/tài liệu, không phải shared runtime package ở phase đầu.
