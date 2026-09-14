# Phân Chia Vai Trò Dự Án — IT Helpdesk Agent (Day 04 Lab)

Tài liệu này định nghĩa chi tiết các vai trò (Roles), trách nhiệm kỹ thuật, các file phụ trách chính và tiêu chí nghiệm thu cho từng thành viên trong nhóm (quy mô 4 – 5 người).

---

## Bảng Phân Công Tổng Quan

| Role | Tên vai trò | Trách nhiệm trọng tâm | Artifact / Files chính phụ trách |
|---|---|---|---|
| **Role 1** | **Team Lead & System Prompt Engineer** | Quản lý repo, điều phối, tối ưu hóa `system_prompt.md` (v0 $\rightarrow$ v3) | `starter_v0/artifacts/system_prompt.md`<br>`TEAMMATES.md`<br>`starter_v0/artifacts/REPORT.md` (A, C1, C3) |
| **Role 2** | **Tool Interface & Registry Engineer** | Tối ưu schema `tools.yaml`, đồng bộ tool registry, quản lý `version_log.csv` | `starter_v0/artifacts/tools.yaml`<br>`starter_v0/artifacts/version_log.csv`<br>`starter_v0/tools/__init__.py` |
| **Role 3** | **QA, Benchmark & Dataset Designer** | Chạy eval base, phân tích failure, xây dựng bộ 10 cases `eval_group.json` | `starter_v0/data/eval_group.json`<br>`starter_v0/run_eval.py`<br>`starter_v0/artifacts/REPORT.md` (B1, B2, B3) |
| **Role 4** | **Security & Red-Teaming Engineer** | Kiểm thử tấn công (adversarial suite), xây dựng guardrails 2 lớp, bảo mật | `starter_v0/data/eval_adversarial.json`<br>`starter_v0/artifacts/REPORT.md` (B4a, B6)<br>`starter_v0/tools/` (guardrail validation) |
| **Role 5** | **UI Developer & Demo / Bonus Tool** | Xây dựng Chat UI (Streamlit), kịch bản demo, chuẩn bị bonus tool (nếu có) | `starter_v0/app.py` (hoặc UI code)<br>`starter_v0/chat.py`<br>`starter_v0/tools/<bonus_tool>/` (optional) |

> **Lưu ý nếu nhóm có 4 người:** Role 5 có thể gộp phần **UI Developer** cho Role 1/Role 2, và phân bổ phần **Demo/Bonus Tool** cho Role 3/Role 4.

---

## Chi Tiết Nhiệm Vụ Từng Thành Viên

### 👤 Role 1: Team Lead & System Prompt Engineer
- **Mục tiêu:** Định hình "bộ não" của agent, đảm bảo agent hiểu đúng danh tính, tôn trọng các quy tắc hội thoại và ranh giới an toàn.
- **Nhiệm vụ cụ thể:**
  1. **Quản trị repository:** Tạo fork, phân quyền, cấu hình branch nộp bài, review và merge pull requests từ các thành viên (**không dùng squash merge** để giữ commit cá nhân).
  2. **Tối ưu `system_prompt.md`:** 
     - Xây dựng các phiên bản từ `v0` (baseline) đến `v3`.
     - Bổ sung quy tắc: Không tự đoán identifier (`asset_id`, `employee_id`), bắt buộc hỏi lại (`clarify`) khi thiếu thông tin.
     - Xử lý ngữ cảnh đa lượt (multi-turn): Nhận biết khi người dùng sửa đổi (correction) hoặc hủy yêu cầu (cancellation).
     - Định dạng output JSON nhất quán (`intent`, `action`, `reply`, `evidence_ids`).
  3. **Viết báo cáo:** Điều phối nội dung `REPORT.md` (Phần A - Giới thiệu agent, Phần C1 - Reflection chung của nhóm, Phần C3 - Final checkout).

---

### 👤 Role 2: Tool Interface & Registry Engineer
- **Mục tiêu:** Thiết kế giao diện công cụ chuẩn xác để model chọn đúng công cụ và truyền đúng tham số (arguments).
- **Nhiệm vụ cụ thể:**
  1. **Tối ưu `tools.yaml`:**
     - Hoàn thiện description cho từng tool (mô tả rõ tool sở hữu loại dữ liệu gì, khi nào nên dùng và khi nào KHÔNG dùng).
     - Chuẩn hóa schema tham số: định nghĩa rõ `type`, `enum` hợp lệ, các trường `required`, default values.
     - Phân định rõ ràng: ranh giới giữa kiểm tra dịch vụ dùng chung (`check_service_status`) vs kiểm tra thiết bị đơn lẻ (`inspect_device`).
  2. **Đồng bộ Tool Registry:** Đảm bảo tính nhất quán giữa `tools.yaml`, `tools/__init__.py` và tài liệu `TOOL.md` của từng tool.
  3. **Quản lý Version Tracking:** Cập nhật file `version_log.csv` sau mỗi vòng cải tiến (tính sha256 hash của prompt và tools, ghi hypothesis, metrics before/after và file run tương ứng).

---

### 👤 Role 3: QA, Benchmark & Dataset Designer (Team Eval)
- **Mục tiêu:** Thiết lập thước đo định lượng, phân tích nguyên nhân lỗi và phát triển bộ đánh giá đặc thù của nhóm.
- **Nhiệm vụ cụ thể:**
  1. **Chạy Benchmark & Đánh giá tự động:**
     - Sử dụng `run_eval.py` để chạy đánh giá trên suite `eval_base.json` cho từng version (`v0` -> `v3`).
     - Đảm bảo điều kiện bằng chứng hợp lệ: `provider_error_cases == 0` và `measured_cases == total_cases`.
  2. **Phân tích lỗi (Failure Analysis):**
     - Điền bảng B2 trong `REPORT.md`: phân loại lỗi theo wrong-tool, wrong-arguments, missing-information, multi-turn carry-over.
     - Đề xuất giả thuyết cải tiến (hypothesis) chuyển giao cho Role 1 và Role 2 thực hiện.
  3. **Thiết kế bộ Test riêng (`data/eval_group.json`):**
     - Viết đúng **10 test cases mới (original)**: 5 single-turn và 5 multi-turn.
     - Bao phủ các tình huống khó: người dùng đổi ý giữa chừng, nhập thiếu thông tin, yêu cầu chỉ format dữ liệu, gọi 2 tool cùng loại với args khác nhau.

---

### 👤 Role 4: Security & Red-Teaming Engineer (Adversarial & Guardrails)
- **Mục tiêu:** Bảo vệ agent trước các cuộc tấn công prompt injection, giả mạo trạng thái và ngăn chặn rò rỉ dữ liệu nhạy cảm.
- **Nhiệm vụ cụ thể:**
  1. **Kiểm thử bộ Adversarial (`data/eval_adversarial.json`):**
     - Chạy suite adversarial và phân tích ít nhất 3 security cases (bảng B4a trong `REPORT.md`).
     - Kiểm tra trực tiếp file hệ thống và log: đảm bảo không có ticket nào bị tạo ngoài ý muốn (`starter_v0/tickets/`), không rò rỉ secret.
  2. **Xây dựng Guardrails 2 lớp (Defense-in-Depth):**
     - *Lớp 1 (Prompt & Interface):* Cấm tuân theo instruction nhúng trong bài viết KB, tài liệu policy hoặc web search result.
     - *Lớp 2 (Implementation Guardrail):* Kiểm tra logic trong tool implementation (chặn `create_ticket` nếu `confirmed` không phải Boolean `true` thực sự, chặn gửi `asset_id` / `employee_id` / `password` / `token` ra API tìm kiếm ngoài `search_device_info`).
  3. **Viết phần Safety Review:** Hoàn thành mục B6 trong `REPORT.md`.

---

### 👤 Role 5: UI Developer & Demo / Bonus Tool Specialist
- **Mục tiêu:** Trực quan hóa tương tác của agent trên giao diện người dùng và chuẩn bị kịch bản demo thuyết phục.
- **Nhiệm vụ cụ thể:**
  1. **Xây dựng Giao diện Chat (Streamlit):**
     - Tái sử dụng trực tiếp hàm `run_model_tool_loop` từ `chat.py` (không viết agent loop riêng).
     - UI hiển thị rõ ràng: Lời nhắn người dùng, danh sách các tool được gọi + arguments, kết quả thực thi tool hoặc lỗi, câu trả lời cuối cùng, artifact version & hash.
  2. **Chuẩn bị Kịch bản Demo:**
     - Chọn 3 – 5 kịch bản tiêu biểu chứng minh sự khác biệt rõ rệt giữa `v0` (bị sai/lỗi) và `v3` (xử lý thành công).
     - Lưu sẵn fallback run / transcript đề phòng sự cố mạng hoặc lỗi quota API khi demo.
  3. **Xây dựng Bonus Tool (Nếu có thời gian & đăng ký điểm cộng):**
     - Phát triển 1 capability mới hoàn chỉnh (ví dụ: `network_diagnostics`, `approved_software_catalog`, ...).
     - Yêu cầu đủ: Thư mục `tools/<tool_name>/TOOL.md`, code `tool.py`, đăng ký vào `tools/__init__.py`, thêm schema vào `tools.yaml`, có mock data, smoke test và test case minh chứng.

---

## Quy Trình Phối Hợp Trên Git

Mỗi thành viên cần tuân thủ nghiêm ngặt hướng dẫn trong `SUBMISSION-GUIDE.md`:

1. **Cấu hình định danh Git cá nhân trước khi commit:**
   ```powershell
   git config user.name "Họ và Tên"
   git config user.email "email_cua_ban@example.com"
   ```
2. **Tạo branch riêng từ fork chung:**
   ```powershell
   git switch -c contrib/<github_username>
   ```
3. **Thực hiện phần việc, commit rõ ràng:**
   ```powershell
   git add <cac_file_thay_doi>
   git commit -m "feat(scope): mo ta dong gop"
   ```
4. **Push lên GitHub và tạo Pull Request (PR):**
   ```powershell
   git push -u origin contrib/<github_username>
   ```
5. **Merge PR:** Team Lead review và merge PR vào branch chính (**không dùng Squash Merge**).
6. **Kiểm tra trước khi nộp:**
   - Mỗi thành viên **bắt buộc phải có ít nhất 1 commit** trong lịch sử branch nộp bài:
     ```powershell
     git log --format="%h | %an <%ae> | %s"
     ```
   - Mỗi thành viên **tự viết và tự commit** phần Self-Reflection của mình trong mục C2 của file `REPORT.md`.
   - **Tất cả thành viên nộp cùng một URL GitHub của fork chung lên tài khoản VLearn cá nhân**.
