# Tool Folder Contract

Mỗi tool nằm trong thư mục riêng:

```text
tools/<tool_name>/
  TOOL.md
  tool.py
```

`tools/__init__.py` là registry dùng chung cho eval, CLI chat và UI.

Frontmatter tối thiểu của `TOOL.md`:

```yaml
---
name: tool_name
track: core | bonus
kind: live_api | local_knowledge | local_status | local_inventory | local_formatter | action | control
provider: optional_provider_name
requires_env: []
inputs: [arg_name]
outputs: [field_name]
side_effect: false | true | local_file_write
requires_confirmation: true
---
```

Chỉ action tool mới dùng `requires_confirmation`. Nếu nhóm chọn làm bonus tool,
tool đó phải dùng dữ liệu giả lập, output JSON ổn định, có lỗi rõ ràng cho input
không tồn tại và có smoke test. Không thêm dữ liệu thật, credential hoặc thông
tin cá nhân.

## Tool & Schema Engineer handoff

Phần này là điểm kiểm soát cho Prompt Lead, Eval Author, Security Lead và Report
Lead khi review đóng góp của Tool & Schema Engineer.

### Phạm vi đã thay đổi

- `artifacts/tools.yaml`: làm rõ positive/negative routing, required arguments,
  enum/format constraints, confirmation boundary và external-data boundary.
- `tools/*/TOOL.md`: đồng bộ inputs, outputs và trust/side-effect contract với
  implementation hiện tại.
- `tools/__init__.py`: đã audit nhưng không thay đổi; 9 declaration names hiện
  đồng bộ với 9 registry keys và không có tên trùng.
- Không thay đổi `system_prompt.md`, evaluator, provider adapter, UI, report,
  version log hoặc tool implementation Python trong phần việc này.

### Hypothesis để Eval Author kiểm chứng

Nếu mỗi declaration nêu rõ dữ liệu tool sở hữu, trường hợp không được dùng,
required routing arguments và boundary khi thiếu thông tin/action/external data,
thì tool-routing accuracy và argument accuracy sẽ tăng mà không làm tăng extra
tool calls hoặc unsafe actions.

Các nhóm case cần so sánh trước/sau:

- status so với device: `H01`, `H02`, `H05`, `H06`, `H13`, `H15`, `H16`;
- KB, policy và formatter: `H03`, `H07`, `H17`, `H20`, `E01-E04`, `E06-E07`;
- missing information: `H10`, `H11`, `H19`, `M01`;
- correction/multi-turn: `M02-M04`, `M06`, `M08`, `M10`;
- confirmation: `H12`, `M05`, `M09`, `E05`, `E08`, `A03-A05`, `A10-A11`;
- internal/external boundary: `E09-E10`, `A06`, `A12`.

### Report Lead control notes

- Report B1 `changed_artifact`: `tools.yaml` and synchronized `TOOL.md` files.
- Report B1 hypothesis: use the hypothesis above; metric values must come only
  from runs where `provider_error_cases == 0` and `measured_cases == total_cases`.
- Report B2: cite concrete before/after traces for wrong tool, wrong argument,
  missing information and extra tool calls; do not claim improvement from prompt
  wording alone.
- Report B6: record that `create_ticket` requires confirmation of the current
  payload and `search_device_info` permits only public product identity.
- Report B7: routing ownership and argument conventions belong in `tools.yaml`;
  conversation-wide correction/cancellation rules remain in `system_prompt.md`.
- The local Gemini preflight passed with structured `check_service_status`
  arguments. The attempted full v0 run was invalid because Gemini free-tier
  quota allowed only 5 requests/minute and produced HTTP 429 errors; its partial
  accuracy must not be reported as baseline evidence.
- Tavily live smoke test passed for public input `Lenovo / ThinkPad T14 Gen 4 /
  drivers`: the tool returned 2 results from `support.lenovo.com`, reported the
  Lenovo official-domain allowlist, and emitted its external-data notice and
  untrusted-web trust boundary. The privacy probe also passed: a model string
  containing `LT-204 EMP-1001` was rejected with
  `restricted_internal_identifier` before any Tavily request could occur.
- Local tools and the no-write `create_ticket` confirmation path were
  smoke-tested successfully. No API key value was printed or written to a
  tracked file during validation.

### Required validation before merge

1. Parse `artifacts/tools.yaml` and confirm exactly 9 unique declarations.
2. Confirm declaration names equal `TOOL_FUNCTIONS` keys.
3. Run `python -m compileall -q .`.
4. Run provider preflight after every schema revision.
5. Run the same provider/model for valid v0 and post-change comparisons.
6. Smoke-test local tools and Tavily separately; never print or commit API keys.
7. Ask Security Lead to inspect external request fields and `tickets/` writes.
8. Ask Report Lead to link only valid run/transcript evidence.

### Known contract observation outside this edit

The model-facing/registry name is `policy`, while `policy/tool.py` currently
returns an inner result field `"tool": "search_company_policy"`. The schema and
registry remain synchronized, so no Python implementation was changed here.
Prompt/Security leads should decide separately whether the inner result field
should be normalized to `policy`.
