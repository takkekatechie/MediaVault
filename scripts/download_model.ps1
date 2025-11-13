<#
PowerShell helper to download a large model file and optionally verify SHA256.
Usage:
  .\download_model.ps1 -Url "https://example.com/deepseek-ocr.gguf" -OutPath "models\deepseek-ocr.gguf" -Sha256 "<sha256>"

This script is intentionally simple and uses built-in PowerShell cmdlets.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$Url,

    [Parameter(Mandatory=$false)]
    [string]$OutPath = "models\deepseek-ocr.gguf",

    [Parameter(Mandatory=$false)]
    [string]$Sha256 = ""
)

try {
    $outDir = Split-Path -Path $OutPath -Parent
    if (-not (Test-Path -Path $outDir)) {
        Write-Host "Creating directory: $outDir"
        New-Item -ItemType Directory -Path $outDir -Force | Out-Null
    }

    $tmp = [System.IO.Path]::GetTempFileName()
    Remove-Item $tmp -Force
    $tmp = "$tmp.download"

    Write-Host "Downloading model from $Url to temporary file $tmp"
    Invoke-WebRequest -Uri $Url -OutFile $tmp -UseBasicParsing -Verbose

    if ($Sha256 -ne "") {
        Write-Host "Verifying SHA256..."
        $hash = Get-FileHash -Path $tmp -Algorithm SHA256
        if ($hash.Hash.ToLower() -ne $Sha256.ToLower()) {
            Write-Error "SHA256 mismatch. Expected: $Sha256, Actual: $($hash.Hash)"
            Remove-Item $tmp -Force -ErrorAction SilentlyContinue
            exit 1
        }
        else {
            Write-Host "SHA256 verified."
        }
    }

    Write-Host "Moving model to: $OutPath"
    Move-Item -Path $tmp -Destination $OutPath -Force
    Write-Host "Download complete: $OutPath"
}
catch {
    Write-Error "Download failed: $_"
    if (Test-Path $tmp) { Remove-Item $tmp -Force -ErrorAction SilentlyContinue }
    exit 1
}
