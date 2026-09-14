param(
    [Parameter(Mandatory = $true)]
    [string]$Version,
    [string]$Provider = "gemini",
    [string]$Model = "",
    [double]$CaseDelaySec = 15
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

$env:DAY04_CASE_DELAY_SEC = "$CaseDelaySec"

$preflightArgs = @("scripts/preflight_provider.py", "--provider", $Provider)
$evalCommon = @("--provider", $Provider, "--version", $Version)
if ($Model) {
    $preflightArgs += @("--model", $Model)
    $evalCommon += @("--model", $Model)
}

Write-Host "Preflight ($Provider $Model) delay=${CaseDelaySec}s..."
python @preflightArgs
if ($LASTEXITCODE -ne 0) {
    throw "Preflight failed. Check API key in .env then retry."
}

Write-Host "Running group suite version=$Version ..."
python run_eval.py @evalCommon --suite group --eval-cases data/eval_group.json
if ($LASTEXITCODE -ne 0) { throw "Group eval failed" }

Write-Host "Running adversarial suite version=$Version ..."
python run_eval.py @evalCommon --suite adversarial --eval-cases data/eval_adversarial.json
if ($LASTEXITCODE -ne 0) { throw "Adversarial eval failed" }

Write-Host "Done. Update artifacts/ROLE_C_*.md with new runs/ paths."
