<#
render_ppt_com.ps1 — render every slide of a .pptx to preview/slide-NN.png using
Microsoft PowerPoint via COM automation. This is the skill's primary renderer on
Windows: PowerPoint draws the slides itself, so the previews match what the user sees
when they open the deck, and it needs neither LibreOffice nor poppler/pdftoppm.

Usage:
  powershell -NoProfile -ExecutionPolicy Bypass -File render_ppt_com.ps1 `
     -Deck  "C:\...\presentation.pptx" `
     -OutDir "C:\...\preview" `
     [-Width 1867] [-Slides "3,7-9"]

Exits non-zero (and prints RENDER_COM_UNAVAILABLE) if PowerPoint COM cannot start,
so the bash wrapper can fall back to LibreOffice.
#>
param(
  [Parameter(Mandatory=$true)][string]$Deck,
  [Parameter(Mandatory=$true)][string]$OutDir,
  [int]$Width = 1867,
  [string]$Slides = ""
)
$ErrorActionPreference = 'Stop'

function Get-RequestedIndices {
  param([string]$Spec, [int]$Count)
  if ([string]::IsNullOrWhiteSpace($Spec)) { return @(1..$Count) }
  $indices = New-Object System.Collections.Generic.List[int]
  foreach ($token in $Spec.Split(',')) {
    $part = $token.Trim()
    if ($part -match '^([0-9]+)-([0-9]+)$') {
      $start = [int]$Matches[1]; $end = [int]$Matches[2]
      if ($start -gt $end) { throw "Invalid slide range: $part" }
      $values = $start..$end
    } elseif ($part -match '^[0-9]+$') {
      $values = @([int]$part)
    } else {
      throw "Invalid slide selection: $part"
    }
    foreach ($value in $values) {
      if ($value -lt 1 -or $value -gt $Count) { throw "Slide out of range: $value (deck has $Count slides)" }
      if (-not $indices.Contains($value)) { [void]$indices.Add($value) }
    }
  }
  return @($indices | Sort-Object)
}

$Deck = (Resolve-Path $Deck).Path
if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir -Force | Out-Null }
$OutDir = (Resolve-Path $OutDir).Path

# Start PowerPoint; if Office isn't installed this throws — signal the wrapper.
try {
  $ppt = New-Object -ComObject PowerPoint.Application
} catch {
  Write-Output 'RENDER_COM_UNAVAILABLE'
  exit 3
}

try {
  # ReadOnly = msoTrue(-1), Untitled = msoFalse(0), WithWindow = msoFalse(0)
  $pres = $ppt.Presentations.Open($Deck, -1, 0, 0)
  $ratio = $pres.PageSetup.SlideHeight / $pres.PageSetup.SlideWidth
  $h = [int][math]::Round($Width * $ratio)
  $indices = @(Get-RequestedIndices -Spec $Slides -Count $pres.Slides.Count)

  if ([string]::IsNullOrWhiteSpace($Slides)) {
    Get-ChildItem -Path $OutDir -Filter 'slide-*.png' -ErrorAction SilentlyContinue | Remove-Item -Force
  } else {
    foreach ($index in $indices) {
      $path = Join-Path $OutDir ('slide-{0:D2}.png' -f $index)
      if (Test-Path $path) { Remove-Item -LiteralPath $path -Force }
    }
  }

  foreach ($index in $indices) {
    $slide = $pres.Slides.Item($index)
    $path = Join-Path $OutDir ('slide-{0:D2}.png' -f $index)
    $slide.Export($path, 'PNG', $Width, $h)
    Write-Output $path
  }
  $pres.Close()
} finally {
  if ($null -ne $pres) {
    try { [System.Runtime.InteropServices.Marshal]::ReleaseComObject($pres) | Out-Null } catch {}
  }
  $ppt.Quit()
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null
}
