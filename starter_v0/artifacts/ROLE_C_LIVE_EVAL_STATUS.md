# Role C — Live eval status

## Blocker

`python scripts/preflight_provider.py --provider openrouter` fails:

```text
RuntimeError: Missing API key env var: OPENROUTER_API_KEY
```

Đã thử live run trên **v0** (version hiện có; A/B chưa có v3 trong repo):

| Suite | measured_cases | provider_error_cases | Local run file (gitignored) |
|---|---:|---:|---|
| adversarial | 0 | 12 | `runs/v0_B_adversarial_openrouter_20260914T184023357070.json` |
| group | 0 | 10 | `runs/v0_B_group_openrouter_20260914T184038892989.json` |

Các run này **không** đủ điều kiện evidence nộp bài. Cần `.env` có key rồi chạy lại `scripts/role_c_run_evals.ps1`.

## Đã chuẩn bị sẵn

1. `data/eval_group.json` — validated với `run_eval.load_cases` + `validate_expected_tools`
2. `scripts/role_c_run_evals.ps1` — preflight → group → adversarial
3. Static adversarial analysis + feedback A/B trong `artifacts/ROLE_C_*.md`

## Khi có key (Role C hoặc bạn có key nhóm)

```powershell
cd starter_v0
# điền OPENROUTER_API_KEY vào .env — không commit
.\.venv\Scripts\python.exe scripts/preflight_provider.py --provider openrouter
.\.venv\Scripts\python.exe run_eval.py --provider openrouter --version v0 --suite adversarial --eval-cases data/eval_adversarial.json
.\.venv\Scripts\python.exe run_eval.py --provider openrouter --version v0 --suite group --eval-cases data/eval_group.json
# Sau A/B: đổi --version v3
```

Cập nhật path `runs/*.json` vào `ROLE_C_HANDOFF.md` và PASS/FAIL vào `ROLE_C_ADVERSARIAL_REVIEW.md`.
