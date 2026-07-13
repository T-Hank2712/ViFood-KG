# Feature Specification: Canonical KG Pipeline

**Feature Branch**: `001-canonical-kg-pipeline`

**Created**: 2026-07-13

**Status**: Draft

**Input**: "Định nghĩa flow chuẩn của ViFood-KG như canonical knowledge core: nguồn dữ liệu đáng tin cậy -> raw snapshot -> extractor -> staging -> transformer -> curated release -> attested manifest -> quality gate -> Neo4j graph. Flow này giữ ranh giới rõ với ViFood-KG-Builder: KG tạo tri thức chuẩn, Builder chỉ match/create runtime theo contract."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Quản lý nguồn dữ liệu chuẩn (Priority: P1)

Là người quản trị knowledge core, tôi muốn mọi nguồn dữ liệu được khai báo trong source registry trước khi dùng, để mỗi node/relationship chuẩn đều truy vết được nguồn.

**Why this priority**: ViFood-KG là nguồn sự thật. Nếu nguồn không rõ, dữ liệu không được xem là tri thức chuẩn.

**Independent Test**: Dùng manifest fixture có source hợp lệ và source chưa đăng ký để xác nhận quality gate chấp nhận hoặc từ chối đúng.

**Acceptance Scenarios**:

1. **Given** một source đã khai báo trong `config/source_registry.yaml`, **When** release manifest tham chiếu source đó, **Then** quality gate có thể xác thực source.
2. **Given** release manifest tham chiếu source chưa đăng ký, **When** quality gate chạy, **Then** release bị từ chối.

---

### User Story 2 - Tạo curated release có provenance (Priority: P1)

Là maintainer dữ liệu, tôi muốn dữ liệu từ raw/staging được transform thành curated nodes/relationships có provenance, để release có thể import vào Neo4j mà không mất trace.

**Why this priority**: Curated release là artifact chính mà Builder và các service khác dựa vào để match entity chuẩn.

**Independent Test**: Build release fixture cho Nutrient/Additive và xác nhận mỗi node nghiệp vụ có relationship `SUPPORTED_BY` tới `Source` hợp lệ.

**Acceptance Scenarios**:

1. **Given** staging records hợp lệ, **When** transformer chạy, **Then** output tạo nodes và relationships đúng ontology.
2. **Given** node nghiệp vụ thiếu provenance, **When** quality gate chạy, **Then** release bị từ chối.

---

### User Story 3 - Import Neo4j idempotent (Priority: P1)

Là người vận hành graph, tôi muốn curated release được import vào Neo4j theo cách idempotent, để chạy lại release không tạo node/relationship trùng.

**Why this priority**: Graph chuẩn cần tái tạo được và an toàn khi reimport.

**Independent Test**: Import cùng release fixture hai lần và xác nhận số node/relationship logic không tăng trùng.

**Acceptance Scenarios**:

1. **Given** curated release hợp lệ, **When** import chạy, **Then** node được merge theo `id`.
2. **Given** cùng release được import lại, **When** import chạy lần hai, **Then** graph không tạo duplicate.

---

### User Story 4 - Công bố contract cho Builder (Priority: P2)

Là developer của ViFood-KG-Builder, tôi muốn ViFood-KG công bố schema/matching contract ổn định, để Builder match `Nutrient` và `Additive` đúng graph chuẩn mà không đoán schema.

**Why this priority**: Hai project giữ riêng vai trò nhưng phải liên kết chặt bằng dữ liệu.

**Independent Test**: Contract fixture mô tả label, relationship, ID format và match keys; Builder có thể dùng contract đó để viết test matching.

**Acceptance Scenarios**:

1. **Given** contract version hợp lệ, **When** Builder kiểm tra compatibility, **Then** Builder biết release/schema nào được hỗ trợ.
2. **Given** contract thiếu match keys cho entity canonical, **When** contract validation chạy, **Then** contract bị xem là incomplete.

### Edge Cases

- Source registry thiếu source trong manifest.
- Raw snapshot hash không khớp manifest.
- Node nghiệp vụ thiếu `SUPPORTED_BY`.
- Alias mơ hồ trỏ nhiều entity.
- Relationship có endpoint không tồn tại.
- Release import lại nhiều lần.
- Builder dùng contract version không tương thích.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: ViFood-KG PHẢI chỉ đưa dữ liệu chuẩn vào graph thông qua curated release.
- **FR-002**: Mọi source dùng trong release PHẢI có trong `config/source_registry.yaml`.
- **FR-003**: Curated release PHẢI có nodes file, relationships file, và attested manifest.
- **FR-004**: Manifest PHẢI ghi source IDs và hash raw snapshot khi có raw source liên quan.
- **FR-005**: Quality gate PHẢI kiểm tra source registry, provenance, endpoint relationship, alias ambiguity, và schema tối thiểu.
- **FR-006**: Node nghiệp vụ chuẩn PHẢI có ID ổn định và không lưu `source`/`source_url` trực tiếp nếu provenance đã nằm trên `Source`.
- **FR-007**: Provenance chuẩn PHẢI dùng `SUPPORTED_BY` hoặc `EVIDENCED_BY` theo ontology.
- **FR-008**: Neo4j import PHẢI merge theo `id` và idempotent.
- **FR-009**: ViFood-KG PHẢI công bố Builder contract mô tả labels, relationships, ID formats, required properties, match keys, alias rules, và supported release IDs.
- **FR-010**: Runtime/AI observations KHÔNG ĐƯỢC tự động trở thành curated knowledge nếu chưa qua pipeline chuẩn.

### Key Entities

- **Source Registry**: Danh sách nguồn được phép dùng.
- **Raw Snapshot**: Bản dữ liệu nguồn lưu lại để kiểm tra.
- **Staging Record**: Dữ liệu trung gian chưa phải tri thức chuẩn.
- **Curated Release**: Bộ nodes/relationships đã review.
- **Attested Manifest**: Metadata release, source IDs và hash.
- **Quality Gate**: Lớp kiểm tra trước import.
- **Canonical Graph**: Neo4j graph chứa tri thức chuẩn.
- **Builder Contract**: Contract để ViFood-KG-Builder match/write đúng schema.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% curated releases hợp lệ có nodes, relationships, và attested manifest.
- **SC-002**: Quality gate từ chối release có source chưa đăng ký.
- **SC-003**: Quality gate từ chối node nghiệp vụ thiếu provenance.
- **SC-004**: Import cùng release hợp lệ hai lần không tạo duplicate logical nodes/relationships.
- **SC-005**: Builder contract mô tả đầy đủ `Nutrient` và `Additive` match keys.

## Assumptions

- Neo4j là target graph chuẩn.
- ViFood-KG giữ vai trò canonical knowledge core.
- ViFood-KG-Builder là consumer/runtime writer và phải tuân theo Builder contract.
- Ingredient chưa là catalog canonical trong ViFood-KG phase hiện tại.
