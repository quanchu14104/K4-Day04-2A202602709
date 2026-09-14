# Phân Chia Vai Trò Nhóm 5 Thành Viên — IT Helpdesk Agent (Day 04 Lab)

> Tài liệu này được chuẩn hóa theo đúng hướng dẫn phân chia vai trò (Phương án Mở rộng — Nhóm 5 thành viên) của Lab Day 04, nhằm tối ưu hóa việc **song song hóa công việc** và đảm bảo bằng chứng commit cho từng thành viên.

---

## Bảng Phân Công Tổng Quan (5 Thành Viên)

| Thành viên | Tên vai trò | Trách nhiệm trọng tâm | Artifacts / Files chính phụ trách |
|:---:|---|---|---|
| **A** | **Prompt Architect / Lead** | Quản lý `system_prompt.md`, chuẩn hóa format JSON, xử lý context carry-over & version hash | `starter_v0/artifacts/system_prompt.md`<br>`starter_v0/artifacts/version_log.csv`<br>`TEAMMATES.md` |
| **B** | **Tool & Schema Engineer** | Quản lý `tools.yaml`, chuẩn hóa enums/arguments, đồng bộ tool name, cấu hình Tavily API | `starter_v0/artifacts/tools.yaml`<br>`starter_v0/tools/__init__.py`<br>`starter_v0/tools/*/TOOL.md` |
| **C** | **Eval Author (G01 $\rightarrow$ G10)** | Tác giả 10 cases `eval_group.json`, chạy benchmark `run_eval.py` & phân tích failure | `starter_v0/data/eval_group.json`<br>`starter_v0/run_eval.py`<br>`starter_v0/artifacts/REPORT.md` (B1, B2, B3) |
| **D** | **UI & Report Lead** | Dựng Live Chat Streamlit, test kịch bản demo rehearsal, tổng hợp báo cáo `REPORT.md` | `starter_v0/app.py` (Streamlit UI)<br>`starter_v0/chat.py`<br>`starter_v0/artifacts/REPORT.md` (Phần A, C1, C3) |
| **E** | **Security & Bonus Tool** | Kiểm thử adversarial, rà soát data leakage (Tavily), kiểm soát tickets rác & code 1 Bonus Tool | `starter_v0/data/eval_adversarial.json`<br>`starter_v0/tickets/`<br>`starter_v0/tools/<bonus_tool>/` (Bonus Tool) |

---

## Chi Tiết Nhiệm Vụ & Tiêu Chí Hoàn Thành

### 👤 Thành viên A: Prompt Architect / Lead
- **Vai trò:** Trưởng nhóm & Kiến trúc sư Prompt
- **Nhiệm vụ chi tiết:**
  1. **Quản lý Repository & Điều phối Git:**
     - Thiết lập repo fork chung, cấp quyền cộng tác cho cả 4 thành viên còn lại.
     - Kiểm tra và duyệt PR từ các nhánh `contrib/<username>` (tuyệt đối **không squash merge** để giữ lịch sử commit cá nhân của từng bạn).
  2. **Tối ưu `system_prompt.md`:**
     - Nâng cấp prompt từ `v0` (baseline) qua `v1`, `v2`, đến `v3`.
     - Quy định các nguyên tắc toàn cục: Không tự đoán `asset_id` hay `employee_id` (bắt buộc dùng `clarify`).
     - Chuẩn hóa định dạng JSON trả về bắt buộc: `intent`, `action`, `reply`, `evidence_ids`.
     - Xử lý ngữ cảnh đa lượt (context carry-over): Nhận diện khi người dùng đính chính (correction) hoặc hủy bỏ (cancellation).
  3. **Quản lý Version Log:** Theo dõi hash SHA-256 của prompt và tool schema trong `version_log.csv`.

---

### 👤 Thành viên B: Tool & Schema Engineer
- **Vai trò:** Kỹ sư Giao diện Công cụ & Tích hợp
- **Nhiệm vụ chi tiết:**
  1. **Quản lý & Tối ưu `tools.yaml`:**
     - Viết lại descriptions rõ ràng cho từng tool: Tool sở hữu dữ liệu gì, khi nào dùng và khi nào **không** dùng.
     - Chuẩn hóa arguments schema: Định nghĩa chặt chẽ `type`, `enum` hợp lệ, các trường `required`, giá trị mặc định.
     - Phân định rõ ràng capability: Phân biệt giữa tra cứu dịch vụ chung (`check_service_status`) vs chẩn đoán thiết bị cụ thể (`inspect_device`).
  2. **Đồng bộ Tool Registry:**
     - Đồng bộ tên tool và tham số giữa `artifacts/tools.yaml`, `tools/__init__.py` và tài liệu `TOOL.md` của từng tool.
  3. **Tích hợp & Kiểm tra Tavily API:**
     - Cấu hình `TAVILY_API_KEY` trong `.env`.
     - Chạy smoke test và kiểm tra hoạt động của `search_device_info`.

---

### 👤 Thành viên C: Eval Author (G01 $\rightarrow$ G10) & Benchmark
- **Vai trò:** Tác giả Bộ Đánh Giá Nhóm & Đảm bảo Chất lượng
- **Nhiệm vụ chi tiết:**
  1. **Thiết kế bộ dữ liệu nhóm `eval_group.json`:**
     - Viết đúng **10 test cases hoàn toàn mới (original)**, đánh mã từ `G01` đến `G10`.
     - Cơ cấu chuẩn: **5 cases single-turn** và **5 cases multi-turn**.
     - Bao phủ các tình huống thực tế: Thay đổi ý định, thiếu mã định danh, gọi nhiều tool cùng lúc, yêu cầu chỉ format dữ liệu.
  2. **Thực thi Benchmark:**
     - Chạy kiểm thử tự động với `run_eval.py` trên bộ `eval_base.json`, `eval_group.json`, `eval_helpdesk_extension.json`.
     - Đảm bảo điều kiện bằng chứng hợp lệ: `provider_error_cases == 0` và `measured_cases == total_cases`.
  3. **Phân tích lỗi (Failure Analysis):**
     - Hoàn thiện Bảng B2 và B3 trong `REPORT.md` (phân loại lỗi routing, wrong args, missing info).

---

### 👤 Thành viên D: UI & Report Lead
- **Vai trò:** Phát triển Giao diện & Điều phối Báo cáo
- **Nhiệm vụ chi tiết:**
  1. **Phát triển Live Chat UI (Streamlit):**
     - Tạo file `app.py` chạy bằng lệnh `streamlit run app.py`.
     - Tái sử dụng trực tiếp hàm `run_model_tool_loop` từ `chat.py` (không viết agent loop riêng).
     - Hiển thị đầy đủ, trực quan: User prompt, tool call name & arguments, kết quả thực thi tool hoặc lỗi, câu trả lời cuối cùng, artifact version & hash.
  2. **Rehearsal Kịch bản Demo:**
     - Chuẩn bị sẵn 3 – 5 kịch bản demo trực tiếp chứng minh sự tiến bộ vượt bậc từ `v0` lên `v3`.
     - Chuẩn bị transcript / fallback run đề phòng mạng hoặc API gặp sự cố lúc chấm.
  3. **Tổng hợp Báo cáo `REPORT.md`:**
     - Chủ trì viết Phần A (Giới thiệu agent, link thử nghiệm, câu hỏi mẫu).
     - Tổng hợp Phần C1 (Reflection chung) và đôn đốc các thành viên tự commit phần C2 (Self-reflection).

---

### 👤 Thành viên E: Security & Bonus Tool Specialist
- **Vai trò:** Chuyên gia Bảo mật & Phát triển Tính Năng Mới
- **Nhiệm vụ chi tiết:**
  1. **Kiểm thử 12 Adversarial Attacks:**
     - Chạy suite `eval_adversarial.json`, đánh giá khả năng chống chịu prompt injection, forged state (user giả lập tool result), instruction nhúng trong KB/Policy.
     - Phân tích chi tiết ít nhất 3 attack cases vào Bảng B4a và B6 trong `REPORT.md`.
  2. **Rà soát Rò Rỉ Dữ Liệu (Data Leakage) & Rác Hệ Thống:**
     - Kiểm tra luồng gọi `search_device_info`: Đảm bảo tuyệt đối không gửi `asset_id`, `employee_id`, serial, hostname, password hay log nội bộ ra ngoài Tavily API.
     - Kiểm tra thư mục `starter_v0/tickets/`: Đảm bảo không sinh ticket rác; tool `create_ticket` chỉ được ghi file khi `confirmed` là Boolean `true` thực sự.
  3. **Phát triển 01 Bonus Tool:**
     - Xây dựng 1 công cụ mới hoàn chỉnh (ví dụ: `network_diagnostics`, `approved_software_catalog`, hoặc `ticket_status_lookup`).
     - Đầy đủ tiêu chuẩn: Thư mục `tools/<bonus_tool>/TOOL.md`, code `tool.py`, đăng ký trong `tools/__init__.py`, khai báo trong `tools.yaml`, mock data và test case minh chứng.

---

## Quy Trình Git & Bằng Chứng Đóng Góp Bắt Buộc

Mọi thành viên cần tuân thủ nghiêm ngặt để đạt điểm tối đa:
1. **Cấu hình Git cá nhân:**
   ```powershell
   git config user.name "Họ và Tên"
   git config user.email "email_github_cua_ban@example.com"
   ```
2. **Tạo nhánh cá nhân:**
   - Thành viên A: `contrib/quanchu14104`
   - Thành viên B: `contrib/<github_user_b>`
   - Thành viên C: `contrib/<github_user_c>`
   - Thành viên D: `contrib/<github_user_d>`
   - Thành viên E: `contrib/<github_user_e>`
3. **Mỗi thành viên phải có ít nhất 1 commit riêng** xuất hiện trong `git log` trên branch chính nộp bài.
4. **Mỗi thành viên tự viết và tự commit** phần Self-reflection của mình (Mục C2 trong `REPORT.md`).
5. **Nộp bài VLearn:** Cả 5 thành viên đều nộp **cùng 1 link GitHub fork chung** trên tài khoản VLearn cá nhân của mình.
