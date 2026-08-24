# Standards and regulatory crosswalk

Snapshot: 2026-08-24. Đây là crosswalk phục vụ học tập, không phải chứng nhận
ISO hay tư vấn pháp lý.

| Lab artifact | Operating purpose | Framework alignment |
|---|---|---|
| `submission.json` product context | Chốt problem, value hypothesis, scope/non-goals, automation level, fallback, reversibility và target milestone. | NIST Govern/Map; ISO/IEC 42001 context, leadership and lifecycle governance ở mức khái niệm. |
| `submission.json` system profile/boundary | Xác định purpose, context, users, affected parties, vendors, data flow và decision impact. | NIST AI RMF Map; ISO/IEC 42005 impact assessment; OECD human-centred values/accountability. |
| Industry Risk Snapshot | Triage năm chiều trước khi phân tích sâu. | NIST Map/Measure; ISO/IEC 23894 risk context. Không dùng để suy ra legal class. |
| `sources.csv` + case briefs | Tạo evidence lineage, giới hạn claim và uncertainty. | NIST Govern/Map; ISO/IEC 42001 documented information/continual improvement ở mức khái niệm. |
| `harm-map.csv` | Nhận diện hazard theo moment, stakeholder, failure mode/layer và impact. | NIST Map/Measure; ISO/IEC 42005 lifecycle impact assessment; OECD fairness/privacy/safety. |
| Controls + residual risk | Chọn preventive/detective/corrective controls và quyết định chấp nhận rủi ro. | NIST Measure/Manage; ISO/IEC 23894; ISO/IEC 42001 Plan–Do–Check–Act. |
| Product requirement + acceptance criteria | Đưa control vào backlog có priority, owner, milestone, evidence và release-blocking decision. | NIST Manage; ISO/IEC 42001 operational planning and documented evidence ở mức khái niệm. |
| Monitoring/trigger/response | Theo dõi production, override, rollback, incident response và re-test. | NIST Measure/Manage; OECD robustness, security, safety and accountability. |
| KPI/KRI + release decision | Cân bằng product value với risk threshold; ghi risk acceptance owner, blocker, condition và re-review trigger. | NIST Govern/Measure/Manage; ISO/IEC 42001 continual improvement. |
| Legal classification + gap plan | Xác định jurisdiction, risk class, obligation, owner, deadline và evidence. | EU AI Act; Vietnam AI Law 134/2025/QH15, Decree 142/2026, Decision 33/2026. |
| Personal-data review | Xác định lawful processing, sensitive data, impact and transfer concerns. | Vietnam Law 91/2025/QH15 + Decree 356/2025; luật privacy của target market khi áp dụng. |
| Optional GenAI security lens | Prompt injection, sensitive disclosure, supply chain, excessive agency và misuse. | OWASP GenAI Security Project; bổ sung, không thay thế impact/legal assessment. |

## Phiên bản dùng trong lab

- NIST AI RMF 1.0 (2023); NIST công bố đang sửa đổi nhưng chưa thay thế bản 1.0.
- NIST AI 600-1 Generative AI Profile (2024).
- ISO/IEC 42001:2023 AI management system.
- ISO/IEC 23894:2023 guidance on AI risk management.
- ISO/IEC 42005:2025 AI system impact assessment.
- OECD AI Principles, cập nhật tháng 5/2024.
- EU AI Act và official implementation timeline hiện hành tại snapshot date.
- Vietnam AI Law/implementing instruments và personal-data law hiện hành tại
  snapshot date.

Không sao chép clause ISO trả phí hoặc tự tuyên bố conformity. Crosswalk chỉ
chuyển tinh thần operating model thành artifact có thể review.
