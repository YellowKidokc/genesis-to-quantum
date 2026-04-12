@echo off
chcp 65001 >nul
title MD Combiner — Theophysics
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
"& {" ^
"  $dir = '%~dp0'.TrimEnd('\');" ^
"  $files = Get-ChildItem -Path $dir -Filter '*.md' | Where-Object { $_.Name -ne 'COMBINED_OUTPUT.md' -and $_.Name -notmatch '^COMBINED_' } | Sort-Object Name;" ^
"  if ($files.Count -eq 0) { Write-Host ''; Write-Host 'No markdown files found in this folder.' -ForegroundColor Red; pause; exit; }" ^
"  Write-Host '';" ^
"  Write-Host '====================================' -ForegroundColor Cyan;" ^
"  Write-Host '   MD COMBINER — Theophysics' -ForegroundColor Cyan;" ^
"  Write-Host '====================================' -ForegroundColor Cyan;" ^
"  Write-Host '';" ^
"  Write-Host \"Found $($files.Count) markdown files:\" -ForegroundColor Green;" ^
"  Write-Host '';" ^
"  $i = 1; foreach ($f in $files) { Write-Host \"  $i. $($f.Name)\" -ForegroundColor White; $i++; }" ^
"  Write-Host '';" ^
"  Write-Host 'How many files per combined output?' -ForegroundColor Yellow;" ^
"  Write-Host '  [2]  [4]  [6]  [8]  [10]  [ALL]' -ForegroundColor White;" ^
"  Write-Host '';" ^
"  $choice = Read-Host 'Enter number (or ALL)';" ^
"  if ($choice -eq 'ALL' -or $choice -eq 'all') { $batchSize = $files.Count; } else { $batchSize = [int]$choice; }" ^
"  if ($batchSize -lt 1) { Write-Host 'Invalid choice.' -ForegroundColor Red; pause; exit; }" ^
"  Write-Host '';" ^
"  Write-Host 'Keep original files?' -ForegroundColor Yellow;" ^
"  Write-Host '  [Y] Yes, keep originals' -ForegroundColor White;" ^
"  Write-Host '  [N] No, delete originals after combining' -ForegroundColor White;" ^
"  $keepChoice = Read-Host 'Keep originals? (Y/N)';" ^
"  $keepOriginals = ($keepChoice -ne 'N' -and $keepChoice -ne 'n');" ^
"  Write-Host '';" ^
"  Write-Host 'Copy each combined file to clipboard?' -ForegroundColor Yellow;" ^
"  Write-Host '  [Y] Yes — pause after each so I can paste' -ForegroundColor White;" ^
"  Write-Host '  [N] No — just save the files' -ForegroundColor White;" ^
"  $clipChoice = Read-Host 'Clipboard mode? (Y/N)';" ^
"  $clipMode = ($clipChoice -eq 'Y' -or $clipChoice -eq 'y');" ^
"  Write-Host '';" ^
"  $totalFiles = $files.Count;" ^
"  $batchNum = 1;" ^
"  for ($start = 0; $start -lt $totalFiles; $start += $batchSize) {" ^
"    $end = [Math]::Min($start + $batchSize, $totalFiles);" ^
"    $batch = $files[$start..($end-1)];" ^
"    $combined = '';" ^
"    foreach ($f in $batch) {" ^
"      $content = Get-Content -Path $f.FullName -Raw -Encoding UTF8;" ^
"      $combined += $content;" ^
"      $combined += \"`n`n---`n`n\";" ^
"    }" ^
"    $outName = \"COMBINED_$($batchNum.ToString('D2'))_of_$([Math]::Ceiling($totalFiles / $batchSize)).md\";" ^
"    $outPath = Join-Path $dir $outName;" ^
"    Set-Content -Path $outPath -Value $combined -Encoding UTF8 -NoNewline;" ^
"    $fileNames = ($batch | ForEach-Object { $_.Name }) -join ', ';" ^
"    Write-Host \"Created: $outName\" -ForegroundColor Green;" ^
"    Write-Host \"  Contains: $fileNames\" -ForegroundColor DarkGray;" ^
"    if ($clipMode) {" ^
"      Set-Clipboard -Value $combined;" ^
"      Write-Host '';" ^
"      Write-Host \"  >> COPIED TO CLIPBOARD. Paste now, then press Enter to continue. <<\" -ForegroundColor Magenta;" ^
"      Read-Host;" ^
"    }" ^
"    if (-not $keepOriginals) {" ^
"      foreach ($f in $batch) { Remove-Item -Path $f.FullName -Force; Write-Host \"  Deleted: $($f.Name)\" -ForegroundColor DarkYellow; }" ^
"    }" ^
"    $batchNum++;" ^
"  }" ^
"  Write-Host '';" ^
"  Write-Host '====================================' -ForegroundColor Cyan;" ^
"  Write-Host '   DONE!' -ForegroundColor Green;" ^
"  Write-Host \"   Created $($batchNum - 1) combined file(s)\" -ForegroundColor Green;" ^
"  if (-not $keepOriginals) { Write-Host '   Originals deleted.' -ForegroundColor DarkYellow; } else { Write-Host '   Originals kept.' -ForegroundColor Green; }" ^
"  Write-Host '====================================' -ForegroundColor Cyan;" ^
"  Write-Host '';" ^
"  pause;" ^
"}"
