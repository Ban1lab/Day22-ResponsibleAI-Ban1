# Day 22 · Responsible AI in Production

Bài lab dành cho học viên đóng vai **Product Manager / Product Owner** chuẩn bị
đưa một AI-enabled product vào production. Bạn không xây model và không viết
ứng dụng. Bạn dùng evidence để biến product risk thành requirement, release
gate, KPI/KRI và một quyết định có người chịu trách nhiệm.

## Nhiệm vụ hôm nay

Trong 150 phút, mỗi học viên chọn một ngành:

- HR / tuyển dụng;
- giáo dục / AI tutor;
- y tế / health assistant;
- mobility / autonomous driving;
- media / news / social / political assistant;
- content creator.

Sau đó bạn nghiên cứu 2–3 case có thật và trả lời câu hỏi cốt lõi:

> Với evidence hiện có, product này nên `go`, `conditional-go`, `no-go` hay chỉ
> tiếp tục ở mức `research-only`?

## Bắt đầu trong 3 phút

Yêu cầu duy nhất: Python 3.10+; không cần API key hoặc cài package.

```bash
git clone https://github.com/VinUni-AI20k/Day22-Responsible-AI-Production-Lab.git
cd Day22-Responsible-AI-Production-Lab
mkdir -p submissions/<MÃ-HỌC-VIÊN>
cp templates/* submissions/<MÃ-HỌC-VIÊN>/
python3 scripts/validate-lab.py submissions/<MÃ-HỌC-VIÊN>
```

Lần chạy đầu **phải fail** vì template còn placeholder. Sửa từng artifact cho
đến khi validator trả về `PASS`.

## Bộ hồ sơ cần nộp

Thư mục `submissions/<MÃ-HỌC-VIÊN>/` gồm đúng sáu artifact:

| Artifact | Product decision mà artifact hỗ trợ |
|---|---|
| `submission.json` | Product Context, System Profile, Risk Snapshot, KPI/KRI, legal classification và release decision. |
| `sources.csv` | Nguồn nào chứng minh claim nào, với giới hạn gì. |
| `case-studies.csv` | 2–3 case có thật, tách verified fact, reported harm và uncertainty. |
| `harm-map.csv` | Ai bị tác động, lỗi bắt đầu ở đâu, control/owner/monitoring là gì. |
| `compliance-gap-analysis.csv` | Risk → product requirement → Given/When/Then → priority → evidence → release blocker. |
| `group-synthesis.csv` | Pattern chung sau khi so sánh các ngành trong nhóm. |

Schema và các enum hợp lệ nằm trong
[lab.config.json](lab.config.json) và [schemas/](schemas/).

## Luồng làm bài 150 phút

| Thời gian | Việc cần chốt |
|---:|---|
| 0–20 | Problem, value hypothesis, scope/non-goals, journey moment, automation và fallback. |
| 20–35 | Industry Risk Snapshot, mỗi chiều 1–5 và có rationale. |
| 35–70 | Research 2–3 case, ghi claim và source trước khi kết luận harm. |
| 70–100 | Harm Map theo stakeholder, failure layer và high-risk moment. |
| 100–130 | Product requirement, acceptance criteria, KPI/KRI và release blockers. |
| 130–145 | Thảo luận nhóm, tìm pattern xuyên ngành. |
| 145–150 | Chạy validator, tự review, commit và push. |

Hướng dẫn đầy đủ: [docs/student-guide.md](docs/student-guide.md). Cách đánh giá:
[docs/rubric.md](docs/rubric.md).

## Cách nộp bài

Tạo repository riêng theo format:

```text
Day22-ResponsibleAI-<MãHV>-<HọVàTên>
```

Ví dụ: `Day22-ResponsibleAI-A0123-NguyenMinhAnh`.

Trước khi nộp:

```bash
python3 scripts/validate-lab.py submissions/<MÃ-HỌC-VIÊN>
python3 -m unittest discover -s tests -v
git status
```

Checklist:

- validator trả về `PASS`;
- không commit CV thật, hồ sơ bệnh án, PII, API key hoặc tài liệu nội bộ;
- mỗi quantitative claim truy ngược được về source;
- mọi `must` có owner, milestone, acceptance evidence và blocker decision;
- `go` không còn release blocker mở;
- commit và push đầy đủ sáu artifact.

## Ví dụ và tài liệu

- Bài mẫu đã đạt kiểm tra cấu trúc: [examples/hr-hiring/](examples/hr-hiring/)
- Cách research và dùng evidence: [docs/research-and-evidence-guide.md](docs/research-and-evidence-guide.md)
- Crosswalk framework/quy định: [docs/standards-crosswalk.md](docs/standards-crosswalk.md)
- Nguồn tham khảo chính thức: [docs/reference-sources.md](docs/reference-sources.md)
- One-page Product Review: [docs/executive-readout-template.md](docs/executive-readout-template.md)

Chạy bài mẫu:

```bash
python3 scripts/validate-lab.py examples/hr-hiring
```

## Quality gate

GitHub Actions chạy unit tests, kiểm tra example và validate mọi thư mục đã
commit dưới `submissions/`. Validator chỉ kiểm tra cấu trúc và traceability. Nó
không fact-check, không chứng minh control có hiệu quả, không phải tư vấn pháp
lý và không tạo ra chứng nhận compliance.
