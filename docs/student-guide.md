# Hướng dẫn sinh viên — PM/PO cho AI in production

## Vai trò và mục tiêu

Bạn đóng vai Product Manager/Product Owner chuẩn bị đưa một AI-enabled product
vào production. Bạn không cần viết code hay huấn luyện model. Kết quả của lab
là một Product Risk & Release Pack giúp team trả lời:

- Product giải quyết vấn đề gì, tạo value nào, scope và non-goals là gì?
- AI ảnh hưởng quyết định nào, ở mức automation nào, fallback ra sao?
- Ai dùng, ai bị tác động dù không dùng, và harm nào đáng lo nhất?
- Case thực tế cho thấy pattern nào?
- Control nào phải trở thành product requirement và acceptance criteria?
- KPI nào đo value, KRI/guardrail nào bảo vệ người dùng và xã hội?
- Gap nào là release blocker, ai có quyền accept residual risk?
- Khi nào phải pause, rollback, re-test hoặc re-classify?

Không dùng dữ liệu cá nhân thật, hồ sơ bệnh án, CV thật, thông tin trẻ em hoặc
tài liệu nội bộ. Không nhập dữ liệu nhạy cảm vào chatbot công cộng.

## Thời lượng gợi ý: 150 phút

1. 0–20 phút — Product Context và AI production boundary.
2. 20–35 phút — Industry Risk Snapshot.
3. 35–70 phút — research 2–3 case có thật.
4. 70–100 phút — Harm Map.
5. 100–130 phút — product backlog, acceptance criteria, KPI/KRI và release gate.
6. 130–145 phút — thảo luận nhóm, tìm pattern chung.
7. 145–150 phút — chạy submission validator.

## Bước 1 — Product Context trước, AI sau

Chọn một ngành từ [lab.config.json](../lab.config.json), rồi điền
`product_context` trong `submission.json`:

- `problem_statement`: vấn đề của user/business, không bắt đầu bằng “cần dùng AI”;
- `value_hypothesis`: outcome kỳ vọng và cách nhận biết value;
- `in_scope` và `non_goals`: chặn scope creep;
- `user_journey_moment`: AI xuất hiện đúng bước nào;
- `product_stage`: discovery, pilot, limited production hay production;
- `automation_level`: decision support, recommendation, semi-automated hoặc
  fully automated;
- `fallback_experience`: user/team làm gì khi AI fail, bị pause hoặc không chắc;
- `decision_reversibility`: quyết định có thể đảo ngược đến mức nào;
- target launch/review date.

Nguyên tắc PM/PO: nếu không mô tả được fallback và owner, chưa sẵn sàng tăng mức
automation.

## Bước 2 — Đóng khung AI production system

Trong `system_profile`, mô tả purpose, user groups, decision impact, data types,
deployment context và target markets. Boundary không dừng ở model:

```text
vendor/input → model/service → product UX → human workflow
             → downstream decision → affected people/society
```

Ghi rõ application/UX, people, vendors, upstream inputs và downstream decisions.
Đặc biệt tìm người bị tác động nhưng không phải user/customer.

## Bước 3 — Industry Risk Snapshot

Chấm từng chiều 1–5; không cộng thành “điểm compliance”.

| Điểm | Product anchor |
|---|---|
| 1 | Tác động nhỏ, dễ đảo ngược, ít dữ liệu nhạy cảm, fallback và review rõ. |
| 3 | Tác động đáng kể hoặc nhóm dễ tổn thương; có thể sửa nhưng tốn thời gian/chi phí. |
| 5 | Ảnh hưởng quyền, sức khỏe, sinh mạng, sinh kế hoặc quy mô lớn; khó đảo ngược. |

Năm chiều: harm severity, high-stakes, sensitive data, affected scale và human
review need. `rationale` phải gắn với product context. Risk score là triage,
không phải legal classification.

## Bước 4 — Research 2–3 case có thật

Mỗi case cần ba lớp:

- `verified_facts`: nguồn thực sự xác nhận điều gì;
- `reported_harm`: harm đã xảy ra, allegation hay foreseeable hazard;
- `limitations`: điều chưa biết hoặc nguồn chưa đủ chứng minh.

Điền `sources.csv` trước, rồi dùng `source_id` dạng `SRC-01` trong
`case-studies.csv`. Không biến allegation thành finding. Không dùng con số nếu
không chỉ ra source, denominator, population và time window khi có.

Xem [research-and-evidence-guide.md](research-and-evidence-guide.md).

## Bước 5 — Harm Map ở product journey moment

Mỗi case có ít nhất một harm row; thêm dòng khi stakeholder hoặc harm khác nhau.

1. Chọn `high_risk_moment` trong journey.
2. Xác định stakeholder và stakeholder type.
3. Chọn failure mode và layer bắt đầu lỗi: UX, grounding, safety, model, data,
   integration/tooling hay governance/process.
4. Mô tả harm cụ thể; chấm severity, likelihood, scale và frequency 1–5.
5. Ghi existing controls và proposed controls.
6. Mô tả human oversight có ý nghĩa: ai review, lúc nào, evidence gì, quyền
   override/pause nào.
7. Chấm residual severity/likelihood.
8. Chốt owner, monitoring metric, threshold và response action.

Human-in-the-loop không có thời gian, quyền hoặc thông tin để sửa quyết định chỉ
là “rubber stamp”, không phải control.

## Bước 6 — Từ harm sang Product Backlog và Release Gate

Mỗi gap/control quan trọng trở thành một dòng
`compliance-gap-analysis.csv`:

- `product_risk_or_requirement`: vấn đề cần đóng;
- `current_state`: bằng chứng hiện có;
- `product_requirement`: capability/process bắt buộc, không mô tả code;
- `acceptance_criteria`: Given / When / Then có thể demo, review hoặc audit;
- `priority`: MoSCoW (`must`, `should`, `could`, `wont-this-release`);
- `release_blocking`: `yes` nếu chưa đạt thì không được release;
- product/control owner, target milestone, deadline/trigger, status;
- evidence cần có và source IDs.

Ví dụ PM/PO:

```text
Given một quyết định loại ứng viên được đề xuất
When recruiter mở release-candidate workflow
Then hệ thống không thể hoàn tất rejection nếu thiếu human review record,
reason code và appeal path.
```

Không viết task dev kiểu “thêm API” hoặc control mơ hồ kiểu “cẩn thận hơn”. PO
định nghĩa outcome, rule, acceptance evidence và gate; team kỹ thuật chọn cách
implement.

## Bước 7 — KPI, KRI và Release Decision

Trong `product_metrics`, chốt bốn dòng:

- `success_kpi`: outcome/value metric + target;
- `risk_kri`: leading/lagging risk indicator + target;
- `guardrail_metric`: hard limit không được trade-off để tăng KPI;
- `review_cadence`: lịch review và event trigger.

Trong `release_decision`, ghi Product Owner, risk acceptance owner, independent
reviewer, decision (`go`, `conditional-go`, `no-go`, `research-only`), blockers,
conditions, residual-risk rationale và next review trigger.

`conditional-go` không có condition/owner/evidence cụ thể là `no-go` trá hình.

## Bước 8 — Compliance classification

Đánh giá Việt Nam và EU độc lập trong `submission.json`. Dùng
`uncertain-requires-legal-review` khi thiếu dữ kiện. Không suy ra legal class từ
Industry Risk Snapshot. Với high-risk hoặc dữ liệu nhạy cảm, legal/privacy
review phải xuất hiện như release gate.

Đây là bài học, không phải tư vấn pháp lý.

## Bước 9 — Thảo luận nhóm

Cả nhóm chốt một dòng `group-synthesis.csv`:

- ngành nào high-stakes nhất;
- harm nào lặp lại;
- layer nào thường bắt đầu lỗi;
- quyết định nào bắt buộc human-in-the-loop;
- guardrail nào dùng xuyên ngành;
- pattern nào thay đổi release roadmap;
- evidence nào hỗ trợ kết luận.

## Bước 10 — Validate và tự review

```bash
python3 scripts/validate-lab.py submissions/<student-id>
```

Exit code `0` chỉ nghĩa hồ sơ đủ cấu trúc. Trước khi nộp, PM/PO phải tự hỏi:

- Mỗi `must` có acceptance criteria và owner chưa?
- Release blockers có nằm trong release decision không?
- KPI có thể tăng trong khi user bị harm không? Nếu có, guardrail ở đâu?
- Fallback có thật sự dùng được trong production không?
- Incident, scope/vendor/data/market change nào buộc re-review?

Nếu cần trình bày với Product/Risk Review Board, dùng
[executive-readout-template.md](executive-readout-template.md) để chốt decision
trong một trang; không copy toàn bộ worksheet lên slide.
