# Ontology ViFood-KC

Ontology của ViFood-KC mô tả cách tri thức thực phẩm đóng gói được biểu diễn trong Neo4j. Mục tiêu của ontology là giúp các hệ thống khác hiểu đúng các term trên nhãn thực phẩm, liên kết chúng về thực thể chuẩn và truy xuất giải thích có nguồn.

## Nguyên tắc chung

Mỗi node chuẩn đều có các thuộc tính nền tảng:

- `id`: mã nội bộ ổn định trong graph.
- `name`: tên chuẩn.
- `reviewed_at`: ngày dữ liệu được review/release.
- `status`: trạng thái dữ liệu, ví dụ `active` hoặc `deprecated`.

Các thuộc tính chuyên biệt như `name_vi`, `ins`, `external_code` hoặc `source_iri` được thêm tùy loại node.

Thông tin có bản chất là quan hệ nên được biểu diễn bằng relationship, không nhồi vào property. Provenance cũng đi qua relationship tới `Source`, nên node nghiệp vụ không có property `source` hoặc `source_url`.

## Node labels

| Label | Ý nghĩa |
|---|---|
| `Nutrient` | Dưỡng chất hoặc thành phần dinh dưỡng chuẩn, có mã định danh từ nguồn dinh dưỡng. |
| `Additive` | Phụ gia thực phẩm chuẩn, có thể có mã INS, E-number, tên và chức năng công nghệ. |
| `FunctionalClass` | Chức năng công nghệ của phụ gia, ví dụ chất bảo quản, chất tạo màu, chất điều chỉnh độ acid. |
| `FoodCategory` | Nhóm thực phẩm, đặc biệt là nhóm pháp lý dùng để biểu diễn quy định phụ gia. |
| `Allergen` | Dị ứng nguyên thực phẩm hoặc nhóm chất gây không dung nạp được chuẩn hóa từ nguồn như Codex CXS 1-1985. |
| `Alias` | Tên gọi khác hoặc token dùng để map text trên nhãn về thực thể chuẩn. |
| `HealthClaim` | Claim sức khỏe có `claim_text`, điều kiện áp dụng, mức bằng chứng và nguồn bằng chứng. |
| `HealthOutcome` | Kết quả sức khỏe hoặc tác động sức khỏe được claim đề cập. |
| `Regulation` | Văn bản pháp lý hoặc tài liệu quy định. |
| `Source` | Nguồn dữ liệu, nguồn pháp lý hoặc nguồn bằng chứng khoa học. |

## Relationship types

| Relationship | Ý nghĩa |
|---|---|
| `SUPPORTED_BY` | Liên kết một thực thể chuẩn với nguồn hỗ trợ nó. |
| `REFERS_TO` | Liên kết `Alias` đến đúng một thực thể chuẩn. |
| `HAS_FUNCTION` | Liên kết `Additive` với `FunctionalClass`. |
| `PERMITTED_IN` | Liên kết `Additive` với `FoodCategory` mà phụ gia được phép dùng theo quy định. |
| `COMMON_IN` | Biểu diễn phụ gia hoặc thành phần thường gặp trong nhóm thực phẩm theo nguồn quan sát phù hợp. |
| `OBSERVED_IN` | Biểu diễn việc một chất/thành phần được quan sát thấy trong nhãn hoặc dữ liệu product layer. |
| `GOVERNS` | Liên kết `Regulation` với phạm vi pháp lý hoặc nhóm đối tượng mà văn bản quy định. |
| `SUPERSEDES` | Liên kết văn bản pháp lý mới với văn bản cũ mà nó thay thế hoặc hợp nhất. |
| `SUBJECT_OF` | Liên kết subject của `HealthClaim`, ví dụ một `Nutrient` hoặc `Additive`. |
| `OUTCOME` | Liên kết `HealthClaim` với `HealthOutcome`. |
| `EVIDENCED_BY` | Liên kết `HealthClaim` với `Source` chứa bằng chứng; nội dung bằng chứng nằm trên node claim, không lặp lại trên relationship. |

## Additive và quy định

Additive biểu diễn phụ gia thực phẩm chuẩn. Phụ gia có thể có:

- mã INS.
- E-number.
- tên chuẩn.
- tên tiếng Việt.
- chức năng công nghệ.
- quy định sử dụng theo nhóm thực phẩm.

Các quan hệ chính:

```text
(:Additive)-[:HAS_FUNCTION]->(:FunctionalClass)
(:Additive)-[:PERMITTED_IN]->(:FoodCategory)
(:Additive)-[:SUPPORTED_BY]->(:Source)
(:Alias)-[:REFERS_TO]->(:Additive)
```

`PERMITTED_IN` là quan hệ pháp lý. Nó không có nghĩa là phụ gia đó chắc chắn xuất hiện trong mọi sản phẩm thuộc nhóm đó. Nó chỉ biểu diễn việc phụ gia được phép dùng trong điều kiện được quy định.

## Allergen

Allergen biểu diễn các nhóm dị ứng nguyên/dị ứng không dung nạp cần nhận diện trên nhãn thực phẩm đóng gói. Nguồn chính hiện tại là Codex CXS 1-1985.

Các quan hệ chính:

```text
(:Allergen)-[:SUPPORTED_BY]->(:Source)
(:Alias)-[:REFERS_TO]->(:Allergen)
```

## Nutrient và HealthClaim

Nutrient biểu diễn dưỡng chất hoặc thành phần dinh dưỡng chuẩn. Nutrient có thể được liên kết đến HealthClaim để mô tả tác động sức khỏe có bằng chứng.

Các quan hệ chính:

```text
(:HealthClaim)-[:SUBJECT_OF]->(:Nutrient)
(:HealthClaim)-[:OUTCOME]->(:HealthOutcome)
(:HealthClaim)-[:EVIDENCED_BY]->(:Source)
(:Nutrient)-[:SUPPORTED_BY]->(:Source)
```

HealthClaim không phải lời khuyên y tế cá nhân. Nó là tri thức có điều kiện, có nguồn và có phạm vi áp dụng.

`HealthClaim` dùng `claim_text` làm nội dung claim. Không tạo thêm `name` nếu giá trị chỉ trùng với `claim_text`.

## Alias và entity linking

Alias giúp map text trên nhãn về thực thể chuẩn. Ví dụ:

```text
“INS 330” -[:REFERS_TO]-> phụ gia tương ứng
```

Alias không được dùng để tạo thêm node trùng nghĩa. Nếu alias trùng với `name`, `name_vi`, `ins` hoặc `external_code`, alias đó không cần tồn tại.

Alias mơ hồ phải được xử lý cẩn thận. Một alias không nên tự động trỏ đến nhiều thực thể chuẩn trong curated graph.

## Phân biệt các quan hệ quan sát và pháp lý

ViFood-KC phân biệt rõ:

- `PERMITTED_IN`: được phép theo quy định.
- `COMMON_IN`: thường gặp theo nguồn quan sát hoặc dữ liệu đáng tin cậy.
- `OBSERVED_IN`: quan sát thấy trên nhãn hoặc product layer.

Ba quan hệ này không thay thế nhau. Một chất được quan sát thấy trên nhãn không tự động chứng minh rằng chất đó được phép dùng. Một chất được phép dùng cũng không có nghĩa là nó xuất hiện trong mọi sản phẩm thuộc nhóm đó.

## Quality gate

Quality gate là lớp kiểm tra trước khi dữ liệu vào Neo4j. Nó bảo vệ graph khỏi dữ liệu thiếu nguồn, sai schema hoặc mơ hồ.

Quality gate kiểm tra:

- node có đủ metadata tối thiểu không.
- source có nằm trong registry và có relationship provenance không.
- manifest có đủ metadata không.
- hash raw snapshot có khớp không.
- relationship có endpoint hợp lệ không.
- alias có mơ hồ không.
- health claim có subject, outcome và evidence không.

Chỉ curated release vượt qua quality gate mới được import vào graph.
