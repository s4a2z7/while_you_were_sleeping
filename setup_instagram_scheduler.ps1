# ================================================
# Instagram 자동 포스팅 - Task Scheduler 자동 설정
# 관리자 권한으로 실행해야 합니다
# ================================================

# 관리자 권한 확인
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "⚠️  관리자 권한이 필요합니다!" -ForegroundColor Yellow
    Write-Host "PowerShell을 관리자 권한으로 다시 실행하세요." -ForegroundColor Yellow
    Read-Host "엔터를 누르세요"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "📱 Instagram 자동 포스팅 설정" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# 스크립트 경로
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$batchFile = "$scriptPath\post_instagram.bat"
$logDir = "$scriptPath\logs"

Write-Host "[1/3] 파일 확인..."

# Batch 파일 확인
if (-not (Test-Path $batchFile)) {
    Write-Host "❌ post_instagram.bat을 찾을 수 없습니다!" -ForegroundColor Red
    Write-Host "   경로: $batchFile" -ForegroundColor Red
    exit 1
}

Write-Host "✅ post_instagram.bat 확인됨" -ForegroundColor Green
Write-Host "   경로: $batchFile" -ForegroundColor Gray

# 로그 폴더 생성
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir | Out-Null
    Write-Host "✅ 로그 폴더 생성됨" -ForegroundColor Green
} else {
    Write-Host "✅ 로그 폴더 이미 존재함" -ForegroundColor Green
}

Write-Host ""
Write-Host "[2/3] Task Scheduler 작업 생성..."

# 기존 작업 확인
$taskName = "Instagram Daily Posting"
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "⚠️  기존 작업이 있습니다. 삭제하고 다시 생성합니다..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "✅ 기존 작업 삭제됨" -ForegroundColor Green
}

# Task Scheduler Action 설정
$action = New-ScheduledTaskAction `
    -Execute "$batchFile" `
    -WorkingDirectory "$scriptPath"

# 매일 07:10 AM 트리거
$trigger = New-ScheduledTaskTrigger `
    -Daily `
    -At "07:10 AM"

# Task 설정
$principal = New-ScheduledTaskPrincipal `
    -UserId "SYSTEM" `
    -LogonType ServiceAccount `
    -RunLevel Highest

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable

# Task 등록
Register-ScheduledTask `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Settings $settings `
    -TaskName $taskName `
    -Description "Post daily briefing to Instagram at 07:10 AM (after GitHub Actions completion at 07:00 AM)" `
    -Force | Out-Null

Write-Host "✅ Task Scheduler 작업 생성됨" -ForegroundColor Green
Write-Host "   작업명: $taskName" -ForegroundColor Gray
Write-Host "   시간: 매일 07:10 AM" -ForegroundColor Gray
Write-Host "   실행: $batchFile" -ForegroundColor Gray

Write-Host ""
Write-Host "[3/3] 설정 확인..."

# 작업 확인
$task = Get-ScheduledTask -TaskName $taskName
$triggers = $task | Get-ScheduledTaskTrigger

if ($task) {
    Write-Host "✅ Task Scheduler 설정 완료!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 작업 정보:" -ForegroundColor Cyan
    Write-Host "   작업명: $($task.TaskName)" -ForegroundColor Gray
    Write-Host "   상태: $($task.State)" -ForegroundColor Gray
    Write-Host "   설명: $($task.Description)" -ForegroundColor Gray
    Write-Host "   트리거: $(if ($triggers) { $triggers.StartBoundary } else { '없음' })" -ForegroundColor Gray
} else {
    Write-Host "❌ Task Scheduler 설정 실패" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ 설정 완료!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📅 자동 실행 일정:" -ForegroundColor Cyan
Write-Host "   시간: 매일 07:10 AM" -ForegroundColor Gray
Write-Host "   작업: Instagram에 브리핑 이미지 자동 포스팅" -ForegroundColor Gray
Write-Host ""
Write-Host "📝 로그 위치:" -ForegroundColor Cyan
Write-Host "   $logDir\instagram_posting.log" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 다음 단계:" -ForegroundColor Cyan
Write-Host "   1. GitHub Actions도 설정하세요 (데이터 수집용)" -ForegroundColor Gray
Write-Host "   2. 매일 아침 자동으로 포스팅됩니다" -ForegroundColor Gray
Write-Host "   3. 로그에서 실행 현황을 확인할 수 있습니다" -ForegroundColor Gray
Write-Host ""

Read-Host "엔터를 누르세요"
