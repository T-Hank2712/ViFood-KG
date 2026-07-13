# Research: Canonical KG Pipeline

## Goal

Chốt ViFood-KG là canonical knowledge core: chỉ dữ liệu qua source registry, curated release, attested manifest và quality gate mới được import thành tri thức chuẩn.

## Decision 1: Keep curated pipeline as source of truth

**Decision**: Mọi tri thức chuẩn phải đi qua raw/staging/curated release/quality gate.

**Rationale**: Giữ graph chuẩn reproducible, có provenance và kiểm soát nguồn.

**Alternatives considered**:

- Cho runtime service ghi trực tiếp canonical graph: nhanh nhưng phá bản chất chuẩn.
- Dùng AI output làm curated data: không có source registry/quality gate.

## Decision 2: Builder contract is public output of KG

**Decision**: ViFood-KG công bố contract để Builder biết schema và match keys.

**Rationale**: Hai repo giữ riêng nhưng không lệch dữ liệu.

**Alternatives considered**:

- Builder tự đọc tùy ý từ graph: dễ lệch schema.
- Gộp hai project: làm mờ ranh giới canonical/runtime.

## Decision 3: Runtime observations remain outside curated release

**Decision**: Quan sát từ AI/runtime không tự động vào curated releases.

**Rationale**: Curated data cần nguồn chuẩn và review.

**Alternatives considered**:

- Tự động promote missing entity từ Builder vào KG: rủi ro nhiễu dữ liệu.
- Không lưu runtime observation: mất khả năng vận hành Builder; phần này thuộc Builder, không thuộc KG core.

## Open Questions

Không còn open question bắt buộc cho phase contract/spec.
