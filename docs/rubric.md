# Rubric bài lab Responsible AI in Production

Tổng điểm: 100. Validator pass là điều kiện cần, không tự động tạo điểm.

| Hạng mục | Điểm | Bằng chứng đạt |
|---|---:|---|
| Product Context và AI boundary | 15 | Problem/value rõ; scope/non-goals; journey moment; automation; fallback; reversibility; affected non-user. |
| Case research và evidence | 20 | 2–3 case; claim đúng mức; số liệu truy vết được; uncertainty/limitations trung thực. |
| Risk Snapshot và Harm Map | 20 | High-risk moment, stakeholder, failure mode/layer, harm và ratings gắn với product context. |
| Product controls và backlog | 20 | Requirement không khóa cách implement; Given/When/Then; MoSCoW; release blocker; owner/milestone/evidence. |
| KPI/KRI và release governance | 15 | Success KPI, risk KRI, hard guardrail, fallback, residual risk, decision, conditions và re-review trigger. |
| Compliance gap plan | 5 | Jurisdiction/scope rõ; legal uncertainty trung thực; review gate và nguồn hiện diện. |
| Group synthesis và communication | 5 | Pattern xuyên ngành có evidence và tác động rõ đến roadmap/release. |

## Mức chất lượng

- **90–100:** có thể dùng làm product review pack; evidence và risk acceptance rõ.
- **75–89:** đủ decision chain; một số metric, criteria hoặc owner còn chung chung.
- **60–74:** harm analysis tốt nhưng chưa chuyển thành backlog/release control.
- **Dưới 60:** AI-first, thiếu source, fallback, owner hoặc release gate; hoặc suy
  diễn legal classification từ risk score.

## Những lỗi làm bài chưa thể release

- Claim định lượng không có source hoặc biến allegation thành fact.
- Chỉ phân tích model mà bỏ qua UX, data, people, vendor và downstream decision.
- Human reviewer không có time, information, authority hoặc appeal path.
- Requirement là task kỹ thuật mơ hồ thay vì product outcome có acceptance evidence.
- Success KPI có thể tăng trong khi user harm tăng nhưng không có KRI/guardrail.
- Quyết định `go` còn backlog item `release_blocking=yes` chưa hoàn thành.
