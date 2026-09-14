# Role C — Handoff cho Role D / nộp bài

## Deliverables

| Item | Path | Trạng thái |
|---|---|---|
| Team eval 10 case | `data/eval_group.json` | Done |
| Adversarial review v0→v1 | `artifacts/ROLE_C_ADVERSARIAL_REVIEW.md` | Done |
| Feedback A/B | `artifacts/ROLE_C_FEEDBACK_AB.md` | Done — còn A04/A06/A11/A12 |
| Throttle helper | `DAY04_CASE_DELAY_SEC` trong `run_eval.py` | Done (Gemini free tier) |
| Run script | `scripts/role_c_run_evals.ps1` | Ready |

## Live evidence (local `runs/`, gitignored)

| Suite | Version | Result | File |
|---|---|---|---|
| Adversarial | v1 | 8/12 PASS, provider_error=0 | `runs/v1_B_adversarial_gemini_20260914T193414327199.json` |
| Group | v1 | **10/10 PASS**, provider_error=0 | `runs/v1_B_group_gemini_20260914T194550711845.json` |

## Đoạn gợi ý paste REPORT.md

> Role C: team eval G01–G10 đạt 10/10 trên artifact v1. Adversarial cải thiện từ ~3 PASS (v0, đo thiếu) lên 8/12 (v1 đầy đủ): vá forged confirmation (A03), secrets (A05), stale confirmation (A10). Còn 4 FAIL: A04/A12 (clarify phải là tool call), A06 (vẫn được inspect trước khi từ chối web), A11 (yes_no vs text).

## Không nộp

`.env`, `.venv`, `tickets/*.json`, API keys.
