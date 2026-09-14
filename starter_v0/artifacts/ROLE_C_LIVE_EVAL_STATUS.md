# Role C — Live eval status

## v1 (sau prompt Role A) — OK evidence

| Suite | measured | provider_error | passed | Model |
|---|---:|---:|---:|---|
| adversarial | 12 | 0 | 8 | gemini-3.5-flash |
| group | 10 | 0 | 10 | gemini-3.6-flash |

Files:

- `runs/v1_B_adversarial_gemini_20260914T193414327199.json`
- `runs/v1_B_group_gemini_20260914T194550711845.json`

## Notes

- `gemini-3.5-flash` free tier: ~20 req/day — hết quota sau adversarial → group dùng `gemini-3.6-flash`.
- Throttle: `$env:DAY04_CASE_DELAY_SEC='15'` khi chạy Gemini.

```powershell
cd starter_v0
$env:DAY04_CASE_DELAY_SEC='15'
.\.venv\Scripts\python.exe run_eval.py --provider gemini --version v1 --suite adversarial --eval-cases data/eval_adversarial.json
.\.venv\Scripts\python.exe run_eval.py --provider gemini --model gemini-3.6-flash --version v1 --suite group --eval-cases data/eval_group.json
```
