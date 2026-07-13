# Research: KG Builder Contract

## Decision 1: Contract is versioned data

**Decision**: Công bố contract bằng Markdown và JSON.

**Rationale**: Markdown dễ đọc, JSON dễ validate/consume.

## Decision 2: Nutrient/Additive are canonical catalog entities

**Decision**: Builder match `Nutrient` và `Additive` vào release của ViFood-KG trước khi tạo mới.

**Rationale**: Hai entity này đã có nguồn chuẩn.

## Decision 3: Ingredient is runtime match-or-create

**Decision**: Contract ghi rõ Ingredient chưa có catalog nền trong phase này.

**Rationale**: Tránh Builder giả định có ingredient release trong KG.

## Open Questions

Không còn open question bắt buộc.
