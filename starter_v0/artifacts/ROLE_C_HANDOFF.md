# Role C — Handoff cho Role D / nộp bài

## Deliverables Role C đã xong (offline)

| Item | Path | Trạng thái |
|---|---|---|
| Team eval 10 case | `data/eval_group.json` | Done — 5 single (G01–G05) + 5 multi (G06–G10) |
| Adversarial review notes | `artifacts/ROLE_C_ADVERSARIAL_REVIEW.md` | Draft từ static review; cần cập nhật sau live run |
| Feedback A/B | `artifacts/ROLE_C_FEEDBACK_AB.md` | Done — ưu tiên confirmation + external boundary + secrets |
| Run script | `scripts/role_c_run_evals.ps1` | Ready khi có API key |

## Live evidence (cần OPENROUTER_API_KEY)

Điều kiện README: `provider_error_cases == 0` và `measured_cases == total_cases`.

Hiện preflight thất bại vì thiếu key. Sau khi điền `.env` (không commit):

```powershell
cd starter_v0
.\scripts\role_c_run_evals.ps1 -Version v0
# Khi A/B có version nộp bài:
.\scripts\role_c_run_evals.ps1 -Version v3
```

Gắn path file `runs/*.json` vào đây:

- Adversarial v0 (blocked, provider_error=12): `runs/v0_B_adversarial_openrouter_20260914T184023357070.json`
- Group v0 (blocked, provider_error=10): `runs/v0_B_group_openrouter_20260914T184038892989.json`
- Final v3 sau A/B + có API key: _PENDING_ — chạy `.\scripts\role_c_run_evals.ps1 -Version v3`

## Đoạn gợi ý paste vào REPORT.md (safety review)

> Role C thiết kế 10 case group (routing args, missing ID, format-only, multi-asset, cancel/meta, correction, switch-to-KB, stale confirmation, external drivers). Red-team cố định A01–A12: ưu tiên phân tích A04 (argument smuggling), A06 (internal→web), A10 (stale confirmation). Starter prompt thiếu confirmation và external boundary; `create_ticket` / `search_device_info` đã có lớp chặn ở implementation nhưng prompt/declaration vẫn cần siết để model không gọi sai. Live run evidence: cập nhật sau khi có provider key.

## Không nộp

`.env`, `.venv`, `tickets/*.json` generated, API keys.
