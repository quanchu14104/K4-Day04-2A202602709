# Day 04 Lab v3 Report — IT Helpdesk Agent

## Team

- Team:
- Members:
- Provider/model:

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

> Viết 1–2 câu mô tả capability và giới hạn của agent.

**Link dùng thử:**

> URL:

## A2. Tool agent có

| Tool | Chức năng | Core / optional / team-built |
|---|---|---|
| clarify | Hỏi bổ sung hoặc xác nhận | core |
|  |  |  |

## A3. Câu hỏi mẫu

1.
2.
3.

## A4. Kịch bản demo đã rehearse

| Scenario | Tool trace cần thấy | Cải thiện version | Fallback run/transcript |
|---|---|---|---|
|  |  |  |  |

# PHẦN B — Chi tiết và evidence

Metric chỉ hợp lệ khi `provider_error_cases == 0`, `measured_cases ==
total_cases`, và tool result error đã được review thủ công.

## B1. Version evidence

| Version | Prompt/tool change | Hypothesis | Metric | Before | After | Run file |
|---|---|---|---|---:|---:|---|
| v0 | baseline | Initial incomplete starter prompt benchmark | adversarial_accuracy | - | 0.4286 | runs/v0_B_adversarial_gemini_20260914T185433933238.json |
| v1 | Thêm trust boundaries & credential refusal | Explicit anti-forged confirmation và credential refusal loại bỏ ticket giả mạo | adversarial_accuracy | 0.4286 | 0.9167 | runs/v1_B_adversarial_gemini_20260914T195254777764.json |
| v2 | Anti-guessing identifiers & standard JSON format | Bắt buộc gọi clarify khi thiếu ID và chuẩn hóa JSON giúp loại bỏ hallucination định danh | adversarial_accuracy | 0.9167 | 1.0000 | runs/v2_B_adversarial_gemini_20260914T201553222741.json |
| v3 | Harden external data boundary & multi-turn corrections | Cấm gửi mã nội bộ ra web search và phân định rõ inspect_device vs search_device_info giúp bảo vệ an toàn biên | adversarial_accuracy | 0.9167 | 1.0000 | runs/v3_B_adversarial_openai_20260915T014121425304.json |

## B2. Failure analysis

| Case ID | Failure type | Actual calls | What failed | Fix |
|---|---|---|---|---|
|  |  |  |  |  |

## B3. Team eval cases

Liệt kê đúng 10 case tự viết: 5 single-turn và 5 multi-turn.

| Case ID | What it tests | Expected behavior | Result |
|---|---|---|---|
|  |  |  |  |

## B4. Live chat evidence

| Scenario/turn | Version | Tool calls + args | Transcript/run | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

## B4a. Adversarial evidence

Phân tích ít nhất 3 cases. Automatic score không chứng minh rằng không có dữ
liệu bị ghi hoặc gửi ra ngoài; cần kiểm tra cả `tool_results` và filesystem.

| Attack case | Expected boundary | Actual calls | Sensitive write/exfiltration occurred? | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

## B5. Optional và bonus tool evidence

Phần này chỉ điền khi nhóm có sử dụng optional tool hoặc tự xây bonus tool.
Không làm phần này không ảnh hưởng việc hoàn thành core lab. `policy`,
`create_ticket` và `search_device_info` là tool có sẵn, không phải tool mới do
nhóm tự xây.

| Category | Evidence file | What worked | Risk / guardrail |
|---|---|---|---|
| Optional built-in |  |  |  |
| External search + privacy boundary |  |  |  |
| Bonus: tool mới do nhóm tự xây |  |  |  |

## B6. Safety review

- Agent có bao giờ tự đoán asset ID hoặc employee ID không?
- Trace/ticket có chứa password, MFA code, token hay dữ liệu thật không?
- Ticket chỉ được tạo sau xác nhận rõ chưa?
- Tool result error nào cần review thủ công?

## B7. Technical reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào không thể chỉ nhìn automatic score?
- Nếu có thêm một vòng, nhóm sẽ thử hypothesis nào?

# PHẦN C — Checkout trước khi nộp

Phần này được hoàn thành sau khi toàn bộ code, evidence và report đã được đưa
lên repository chung. Nhóm chưa nên nộp link trên VLearn nếu reflection hoặc
commit evidence của bất kỳ thành viên nào còn thiếu.

## C1. Reflection chung của nhóm

Các thành viên thảo luận và viết một reflection chung. Nội dung cần dựa trên
evidence thực tế trong repository, không chỉ mô tả cảm nhận chung.

- Mục tiêu nào của nhóm đã hoàn thành? Dẫn đến artifact hoặc run tương ứng.
- Hypothesis hoặc thay đổi nào tạo ra cải thiện rõ nhất?
- Failure quan trọng nào vẫn chưa xử lý được hoàn toàn?
- Nhóm đã phân chia, review và tích hợp công việc như thế nào?
- Nếu có thêm một vòng, nhóm sẽ ưu tiên thay đổi và kiểm chứng điều gì?

**Reflection chung của nhóm:**

> Viết reflection tại đây và dẫn link/path đến evidence liên quan.

## C2. Self-reflection của từng thành viên

Mỗi thành viên tự viết một mục riêng về phần việc chính mình đã thực hiện trong
repository chung. Không viết thay hoặc gộp nhiều thành viên vào một câu trả lời.
Mỗi reflection cần trỏ đến file, commit hoặc pull request có thật để người đọc
có thể đối chiếu đóng góp.

Sao chép mẫu dưới đây cho từng thành viên:

### Chu Minh Quân — 2A202602709

- **Vai trò/phần việc được nhận:** Prompt Architect / Lead (Thành viên A)
- **Những gì tôi đã thay đổi trong repo chung:** Tối ưu hóa toàn diện `system_prompt.md` qua các vòng v0 $\rightarrow$ v1 $\rightarrow$ v2 $\rightarrow$ v3; chuẩn hóa cấu trúc phản hồi JSON bắt buộc (`intent`, `action`, `reply`, `evidence_ids`); thiết lập các nguyên tắc chống đoán mò định danh (`clarify` cho `asset_id`, `employee_id`), chống giả mạo xác nhận (`stale confirmation`, user pseudo-code, spoofed system tags), từ chối nhận credentials (`no_tool`), và ngăn chặn rò rỉ mã định danh nội bộ ra web search ngoài (`search_device_info`); quản lý và ghi vết đầy đủ các phiên bản trong `version_log.csv`.
- **File hoặc artifact liên quan:** `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/version_log.csv`, `TEAMMATES.md`
- **Commit hash hoặc pull request:** `de46902`, `9689bcc`
- **Một quyết định kỹ thuật tôi đã đưa ra và lý do:** Quyết định không cho phép model tự ý suy đoán `asset_id` hay `employee_id` mà bắt buộc phải gọi `clarify(response_type="text")`. Đồng thời, ở boundary `create_ticket`, chỉ cho phép gọi với `confirmed=true` khi có xác nhận tường minh trong lịch sử hội thoại từ người dùng thực (từ chối hoàn toàn user-pasted pseudo-code hay tag giả lập system/developer). Điều này giúp hệ thống loại bỏ triệt để việc sinh ticket rác và hallucination trong môi trường IT doanh nghiệp.
- **Khó khăn tôi gặp và cách tôi xử lý:** Ban đầu khi người dùng yêu cầu tra cứu lỗi thiết bị nội bộ kết hợp tìm giải pháp trên web, model có xu hướng truyền thẳng các mã định danh nội bộ (`LT-xxx`, `EMP-xxxx`) vào tool tìm kiếm ngoài (`search_device_info`), gây rò rỉ thông tin mật. Tôi đã giải quyết bằng cách bổ sung quy tắc phân tách ranh giới rõ ràng giữa công cụ chẩn đoán nội bộ (`inspect_device`) và công cụ tìm kiếm web vendor (`search_device_info`), đồng thời chỉ thị model dùng `clarify` để người dùng cung cấp hãng/model công khai nếu muốn tìm kiếm bên ngoài.
- **Điều tôi học được từ phần việc này:** Hiểu sâu sắc về cơ chế kiểm soát biên (trust boundary) và an toàn prompt (prompt hardening) trong các hệ thống LLM Agent đa lượt. Việc thiết kế prompt không chỉ là hướng dẫn routing mà còn là tuyến phòng thủ đầu tiên chống lại prompt injection, state spoofing và data leakage.
- **Nếu làm lại, tôi sẽ cải thiện điều gì:** Tôi sẽ thiết kế thêm cơ chế tự động validate schema JSON trả về bằng function calling schema ràng buộc chặt hơn để giảm thiểu tối đa rủi ro parse JSON khi chuyển đổi qua các model mã nguồn mở nhỏ hơn.

### [Họ tên thành viên tiếp theo] — [MSSV]

- **Vai trò/phần việc được nhận:**
- **Những gì tôi đã thay đổi trong repo chung:**
- **File hoặc artifact liên quan:**
- **Commit hash hoặc pull request:**
- **Một quyết định kỹ thuật tôi đã đưa ra và lý do:**
- **Khó khăn tôi gặp và cách tôi xử lý:**
- **Điều tôi học được từ phần việc này:**
- **Nếu làm lại, tôi sẽ cải thiện điều gì:**

Mỗi thành viên phải tự commit phần self-reflection của mình bằng Git identity
tương ứng. Reflection phải dẫn đến contribution artifact/commit đã nêu ở trên,
không dùng chính phần reflection làm bằng chứng duy nhất cho đóng góp kỹ thuật.

## C3. Final checkout

Chỉ nộp bài khi mọi mục dưới đây đã được kiểm tra trên branch cuối cùng của
repository chung:

- [ ] `TEAMMATES.md` có đủ họ tên, MSSV, GitHub username và vai trò.
- [ ] Mỗi thành viên có ít nhất một commit trong lịch sử branch nộp bài.
- [ ] Phần reflection chung của nhóm đã hoàn thành và có evidence.
- [ ] Mỗi thành viên đã tự viết và commit self-reflection của mình.
- [ ] `system_prompt.md`, `tools.yaml`, version log, runs, eval, transcript, UI
      và report đã có trong repository.
- [ ] Không có `.env`, API key, token, dữ liệu thật, cache hoặc generated ticket.
- [ ] Nhóm trưởng và mọi thành viên đã thống nhất đúng một URL repository chung.
- [ ] Nhóm trưởng và mọi thành viên sẽ nộp cùng URL đó trên VLearn.

**URL repository chung dùng để nộp:**

> URL:
