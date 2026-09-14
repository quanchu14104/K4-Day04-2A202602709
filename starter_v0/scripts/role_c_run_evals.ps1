param(
    [Parameter(Mandatory = $true)]
    [string]$Version,
    [string]$Provider = "openrouter"
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

Write-Host "Preflight ($Provider)..."
python scripts/preflight_provider.py --provider $Provider
if ($LASTEXITCODE -ne 0) {
    throw "Preflight failed. Set OPENROUTER_API_KEY in .env then retry."
}

Write-Host "Running group suite version=$Version ..."
python run_eval.py --provider $Provider --version $Version --suite group --eval-cases data/eval_group.json
if ($LASTEXITCODE -ne 0) { throw "Group eval failed" }

Write-Host "Running adversarial suite version=$Version ..."
python run_eval.py --provider $Provider --version $Version --suite adversarial --eval-cases data/eval_adversarial.json
if ($LASTEXITCODE -ne 0) { throw "Adversarial eval failed" }

Write-Host "Done. Check runs/ and update artifacts/ROLE_C_ADVERSARIAL_REVIEW.md + ROLE_C_HANDOFF.md"
