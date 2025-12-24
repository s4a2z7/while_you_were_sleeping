#!/usr/bin/env powershell
<#
Windows Task Scheduler에 일일 브리핑 작업 등록 스크립트
관리자 권한으로 실행 필요
#>

# 관리자 권한 확인
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "❌ 이 스크립트는 관리자 권한이 필요합니다!" -ForegroundColor Red
    Write-Host "PowerShell을 '관리자 권한으로 실행'해서 다시 시도하세요." -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "📋 Windows Task Scheduler 자동 설정을 시작합니다..." -ForegroundColor Cyan
Write-Host ""

# Python 경로 확인
Write-Host "[1/5] Python 경로 확인 중..." -ForegroundColor Green
$pythonPath = (python -c "import sys; print(sys.executable)") 2>$null

if (-not $pythonPath) {
    Write-Host "❌ Python을 찾을 수 없습니다!" -ForegroundColor Red
    Write-Host "Python이 설치되어 있고 PATH에 등록되어 있는지 확인하세요." -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "✅ Python 경로: $pythonPath" -ForegroundColor Green

# 프로젝트 디렉토리
$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scriptPath = Join-Path $projectDir "run_daily_briefing.py"

Write-Host ""
Write-Host "[2/5] 작업 경로 확인 중..." -ForegroundColor Green
if (-not (Test-Path $scriptPath)) {
    Write-Host "❌ 스크립트를 찾을 수 없습니다: $scriptPath" -ForegroundColor Red
    pause
    exit 1
}
Write-Host "✅ 스크립트 경로: $scriptPath" -ForegroundColor Green

# 기존 작업 확인
Write-Host ""
Write-Host "[3/5] 기존 작업 확인 중..." -ForegroundColor Green
$existingTask = Get-ScheduledTask -TaskName "Daily Stock Briefing" -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "⚠️  기존 작업이 발견되었습니다." -ForegroundColor Yellow
    $choice = Read-Host "기존 작업을 삭제하고 새로 생성하시겠습니까? (Y/N)"
    if ($choice -eq "Y" -or $choice -eq "y") {
        Write-Host "기존 작업 삭제 중..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName "Daily Stock Briefing" -Confirm:$false
        Write-Host "✅ 기존 작업 삭제 완료" -ForegroundColor Green
    } else {
        Write-Host "❌ 작업 설정이 취소되었습니다." -ForegroundColor Yellow
        pause
        exit 0
    }
}

# 작업 스케줄러 작업 등록
Write-Host ""
Write-Host "[4/5] 작업 등록 중..." -ForegroundColor Green

# 작업 스케줄 설정 (매일 오전 7:00)
$trigger = New-ScheduledTaskTrigger -Daily -At 7:00AM
Write-Host "✅ 트리거 설정 완료: 매일 오전 7:00 AM" -ForegroundColor Green

# 작업 작업 설정
$action = New-ScheduledTaskAction `
    -Execute $pythonPath `
    -Argument "`"$scriptPath`"" `
    -WorkingDirectory $projectDir

Write-Host "✅ 작업 설정 완료: Python 스크립트 실행" -ForegroundColor Green

# 작업 설정
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable

Write-Host "✅ 작업 조건 설정 완료" -ForegroundColor Green

# 작업 등록
Write-Host ""
Write-Host "[5/5] 최종 등록 중..." -ForegroundColor Green

$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive -RunLevel Highest

Register-ScheduledTask `
    -TaskName "Daily Stock Briefing" `
    -Trigger $trigger `
    -Action $action `
    -Principal $principal `
    -Settings $settings `
    -Description "매일 주식 브리핑을 생성하고 이메일로 발송합니다." `
    -Force

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "✅ Task Scheduler 설정 완료!" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 작업 정보:" -ForegroundColor Cyan
Write-Host "  • 작업명: Daily Stock Briefing" -ForegroundColor White
Write-Host "  • 일정: 매일 오전 7:00 AM" -ForegroundColor White
Write-Host "  • 실행: $pythonPath $scriptPath" -ForegroundColor White
Write-Host "  • 작업 디렉토리: $projectDir" -ForegroundColor White
Write-Host ""
Write-Host "🔍 수동 테스트:" -ForegroundColor Yellow
Write-Host "  1. Task Scheduler 열기 (Windows + R → taskschd.msc)" -ForegroundColor Gray
Write-Host "  2. '작업 스케줄러 라이브러리' 검색" -ForegroundColor Gray
Write-Host "  3. 'Daily Stock Briefing' 우클릭 → 실행" -ForegroundColor Gray
Write-Host ""
Write-Host "📊 로그 파일:" -ForegroundColor Yellow
Write-Host "  $projectDir\briefing_scheduler.log" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 팁:" -ForegroundColor Cyan
Write-Host "  • 로그 실시간 모니터링: Get-Content `'$projectDir\briefing_scheduler.log`' -Wait" -ForegroundColor Gray
Write-Host "  • 작업 비활성화: Task Scheduler에서 우클릭 -> 비활성화" -ForegroundColor Gray
Write-Host "  • 작업 삭제: Unregister-ScheduledTask -TaskName 'Daily Stock Briefing'" -ForegroundColor Gray
Write-Host ""

pause
