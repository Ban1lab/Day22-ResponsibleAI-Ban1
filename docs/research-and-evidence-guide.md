# Research and evidence guide

## Source hierarchy

Ưu tiên theo claim cần chứng minh, không theo độ nổi tiếng của nguồn:

1. `primary-official`: luật, regulator decision, accident investigation,
   court filing, government report;
2. `primary-peer-reviewed`: paper và dataset/method/result gốc;
3. `first-party`: system card, transparency/safety report của nhà cung cấp;
4. `secondary-reputable`: báo chí hoặc phân tích chuyên môn có biên tập;
5. `other`: chỉ dùng để tìm đầu mối, không dùng một mình cho claim quan trọng.

First-party safety report hữu ích cho method và self-reported metrics nhưng có
xung đột lợi ích. Regulatory finding mạnh cho sự kiện pháp lý nhưng có thể
không chứng minh nguyên nhân kỹ thuật. Paper mạnh cho mẫu nghiên cứu nhưng
không tự động khái quát sang mọi deployment.

## Quy tắc evidence lineage

Mỗi row nguồn có `supports_claim`: viết đúng một câu mô tả claim mà nguồn hỗ
trợ. Trong case/harm/gap, dùng `source_ids` phân tách bằng dấu `;`.

Ví dụ:

```text
SRC-01 supports: EEOC reported that the screening software automatically
rejected more than 200 applicants under the stated age rules.
```

Không viết “AI tuyển dụng có bias” nếu nguồn chỉ mô tả một hệ thống cụ thể.

## Triangulation tối thiểu

Với claim high-stakes hoặc gây tranh cãi, tìm hai góc độc lập khi có thể:

- event/finding: regulator, court, investigator;
- technical mechanism/performance: paper, audit, system/safety report;
- context/impact: affected stakeholder testimony hoặc credible reporting.

Nếu không đủ, giữ claim hẹp và ghi limitation thay vì bù bằng suy đoán.

## Kiểm tra case trước khi dùng

- Có đúng là AI/algorithmic system hay chỉ là rule-based automation?
- Hệ thống đã deploy hay chỉ là prototype?
- Nguồn nói allegation, settlement, finding hay confirmed causal mechanism?
- Con số có denominator, thời gian và population không?
- Harm đã xảy ra, suýt xảy ra hay là foreseeable hazard?
- Có system layer hoặc governance decision nào ngoài model góp phần không?
- Sau sự cố có control, audit hoặc monitoring nào được thêm?

## Sử dụng AI trong research

Có thể dùng chatbot để tạo search terms hoặc tóm tắt sơ bộ. Không cite chatbot.
Mở nguồn gốc, đọc phần liên quan, ghi source metadata và tự viết claim. Không
upload dữ liệu nhạy cảm hoặc tài liệu hạn chế truy cập vào công cụ công cộng.

## Source freshness

Ghi `published_at` và `accessed_at`; dùng `unknown` thay vì đoán nếu nguồn không
công bố ngày. Với luật, guidance, software standard hoặc
ongoing case, kiểm tra trạng thái tại thời điểm nộp. Repo dùng snapshot
2026-08-24; không mặc định snapshot này còn đúng cho học kỳ sau.
