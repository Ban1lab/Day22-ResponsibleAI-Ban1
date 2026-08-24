# Instructor guide — PM/PO AI in production

## Teaching stance

Đây là product governance lab, không phải coding lab. Sinh viên đóng vai PM/PO
chuẩn bị release một AI-enabled product. Không chấm kiến trúc model, prompt hay
code. Chấm chất lượng decision: value/scope, affected stakeholder, evidence,
product requirement, acceptance criteria, priority, release gate, owner,
KPI/KRI, fallback và re-review trigger.

Chuỗi cần chứng minh:

```text
product value + context → affected stakeholder → harm/failure layer
→ product control requirement → acceptance evidence → KPI/KRI
→ go/conditional-go/no-go → monitor/pause/review/re-classify
```

## Learning outcomes

Sau buổi học, sinh viên có thể:

- frame problem/value mà không “AI-first”;
- chọn automation level theo stakes, reversibility và fallback;
- dùng case evidence để định hình product risk, không copy headline;
- chuyển harm/compliance gap thành backlog item có acceptance criteria;
- phân biệt KPI, KRI và hard guardrail;
- lập release decision có blocker, condition và risk acceptance owner;
- xác định event khiến product phải pause, rollback hoặc re-review.

## Chuẩn bị trước lớp

- Chạy `python3 -m unittest discover -s tests -v`.
- Kiểm tra lại ngày/hiệu lực của nguồn pháp lý trong
  [reference-sources.md](reference-sources.md).
- Chia nhóm 4–6 người và phân bổ nhiều ngành trong mỗi nhóm.
- Nhắc rõ: không dùng dữ liệu cá nhân thật; không cite chatbot; không yêu cầu
  kết luận pháp lý chắc chắn.

## Run of show: 150 phút

### 1. Product frame (0–20)

Đặt câu hỏi: “Nếu bỏ chữ AI, problem và value còn rõ không?”. Check product
stage, scope/non-goals, journey moment, automation level, fallback và
reversibility. Không cho qua nếu mục tiêu chỉ là “ứng dụng AI”.

### 2. Risk Snapshot (20–35)

Yêu cầu giải thích hai điểm cao nhất và một điểm còn uncertainty. Nhắc rằng risk
score không quyết định legal class.

### 3. Case research (35–70)

Spot-check một claim định lượng mỗi nhóm. Hỏi: nguồn xác nhận allegation,
settlement, finding hay causal mechanism? Product lesson là gì? Case có cùng
boundary và user journey moment không?

### 4. Harm Map (70–100)

Hỏi “Ai bị tác động nhưng không phải user?” và “Lỗi bắt đầu ở layer nào?”. Kéo
sinh viên ra khỏi phản xạ đổ mọi lỗi cho model.

### 5. Backlog + release decision (100–130)

Mỗi nhóm chọn 2–4 harm/gap quan trọng nhất và viết product requirement. Kiểm tra:

- acceptance criteria có Given/When/Then và evidence quan sát được;
- priority và release-blocking có hợp lý;
- owner có quyền hành động;
- KPI/KRI/guardrail không mâu thuẫn;
- fallback và next review trigger có thể vận hành.

Không chấp nhận task dev (“thêm API”, “fine-tune model”) làm requirement. PM/PO
phải định nghĩa outcome và gate; implementation thuộc engineering refinement.

### 6. Group synthesis + debrief (130–145)

So sánh high-stakes, recurring harm, common failure layer, human review và
cross-industry guardrail. Mỗi nhóm trả lời: “Pattern nào làm thay đổi roadmap
hoặc release decision?”.

### 7. Validation (145–150)

Sinh viên chạy validator. Nhắc rằng structural pass không thay thế product,
domain, legal, privacy hay security review.

## Rubric (100 điểm)

| Hạng mục | Điểm | Bằng chứng đạt |
|---|---:|---|
| Product Context + AI boundary | 15 | Problem/value rõ; scope/non-goals; journey; automation; fallback; reversibility; affected non-user. |
| Case research + evidence | 20 | 2–3 case; claim đúng mức; số liệu truy vết được; uncertainty/limitations trung thực. |
| Risk Snapshot + Harm Map | 20 | High-risk moment, stakeholder, failure mode/layer, harm và ratings gắn với product context. |
| Product controls + backlog | 20 | Requirement không phụ thuộc implementation; Given/When/Then; MoSCoW; release blocker; owner/milestone/evidence. |
| KPI/KRI + release governance | 15 | Success KPI, risk KRI, hard guardrail, fallback, residual risk, decision, conditions và re-review trigger. |
| Compliance gap/action plan | 5 | Jurisdiction/scope rõ; legal uncertainty đúng; review gate và source hiện diện. |
| Group synthesis + communication | 5 | Pattern xuyên ngành có evidence và tác động rõ đến roadmap/release. |

### Mức chất lượng

- 90–100: có thể dùng làm product review pack; evidence và risk acceptance rõ.
- 75–89: đủ decision chain; một số metric/criteria/owner còn chung chung.
- 60–74: harm tốt nhưng chưa chuyển thành backlog/release control.
- dưới 60: AI-first, thiếu source, không có fallback/owner/gate hoặc suy diễn pháp lý.

Validator pass là điều kiện cần, không cộng điểm tự động.

## Release review prompts cho giảng viên

- “Go” dựa trên evidence nào? Ai ký residual risk?
- “Conditional-go” có condition, deadline và owner hay chỉ là trì hoãn no-go?
- Nếu success KPI tăng nhưng KRI xấu đi, product sẽ làm gì?
- Human reviewer có time, information, authority và appeal path không?
- Production incident nào làm pause ngay lập tức?
- Thay đổi vendor/model/data/user group/market nào buộc re-assessment?
- Evidence nào được tạo ở release, evidence nào cần monitor sau release?

## Mandatory escalation gate

Yêu cầu domain/legal/privacy/security review khi có ảnh hưởng sinh mạng/sức
khỏe/quyền; trẻ em/nhóm dễ tổn thương; dữ liệu nhạy cảm; biometric/surveillance;
quyết định tuyển dụng/giáo dục/tín dụng; autonomous control; third-party data
transfer; hoặc agent/tool có thể thực hiện external action.

## Optional executive readout

Cho mỗi nhóm 3 phút trình bày đúng 1 slide:

1. Product value + automation level.
2. Top harm + affected stakeholder.
3. Must-have release blocker + acceptance evidence.
4. KPI/KRI/guardrail.
5. Decision và next review trigger.
