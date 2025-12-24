#!/usr/bin/env powershell
<#
Docker를 이용한 인스타그램 자동 게시 스크립트
Windows Task Scheduler에서 매일 07:30 AM에 실행
#>

# 색상 정의
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Error_ { Write-Host $args -ForegroundColor Red }
function Write-Warning_ { Write-Host $args -ForegroundColor Yellow }
function Write-Info { Write-Host $args -ForegroundColor Cyan }

Write-Info "================================"
Write-Info "🐳 Docker 인스타그램 게시 시작"
Write-Info "================================"

# 1. 환경변수 로드
Write-Info ""
Write-Info "[1/4] 환경변수 로드 중..."
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# .env 파일에서 읽기
$envFile = Join-Path $scriptDir "backend\.env"
if (Test-Path $envFile) {
    Get-Content $envFile | foreach {
        $name, $value = $_.split("=")
        if ($name -and $value) {
            Set-Item -Path "env:$name" -Value $value
        }
    }
    Write-Success "   ✅ .env 파일 로드 완료"
} else {
    Write-Error_ "   ❌ .env 파일을 찾을 수 없습니다: $envFile"
    exit 1
}

# 2. Docker 상태 확인
Write-Info ""
Write-Info "[2/4] Docker 상태 확인..."
$dockerCheck = docker ps 2>$null
if ($?) {
    Write-Success "   ✅ Docker 실행 중"
} else {
    Write-Error_ "   ❌ Docker가 실행되지 않습니다"
    Write-Warning_ "   Docker Desktop을 시작하세요"
    exit 1
}

# 3. 이미지 확인 및 빌드
Write-Info ""
Write-Info "[3/4] Docker 이미지 확인..."
$imageExists = docker images | Select-String "instagram-poster"
if ($imageExists) {
    Write-Success "   ✅ 이미지 존재: instagram-poster"
} else {
    Write-Warning_ "   ⚠️  이미지를 찾을 수 없습니다. 빌드 중..."
    docker build -f Dockerfile.instagram -t instagram-poster .
    if ($?) {
        Write-Success "   ✅ 이미지 빌드 완료"
    } else {
        Write-Error_ "   ❌ 이미지 빌드 실패"
        exit 1
    }
}

# 4. 컨테이너 실행
Write-Info ""
Write-Info "[4/4] 인스타그램 게시 중..."

$outputPath = Join-Path $scriptDir "output"
$imagesPath = Join-Path $outputPath "images"
$dataPath = Join-Path $outputPath "data"

# 경로 존재 확인
if (-not (Test-Path $imagesPath)) {
    Write-Warning_ "   ⚠️  이미지 폴더가 없습니다: $imagesPath"
    Write-Warning_ "   먼저 브리핑을 생성해주세요"
    exit 1
}

# Docker 실행
$result = docker run --rm `
    -e INSTAGRAM_USERNAME=$env:INSTAGRAM_USERNAME `
    -e INSTAGRAM_PASSWORD=$env:INSTAGRAM_PASSWORD `
    -v "$imagesPath`:/app/output/images:ro" `
    -v "$dataPath`:/app/output/data:ro" `
    instagram-poster 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Success ""
    Write-Success "================================"
    Write-Success "✅ 인스타그램 게시 성공!"
    Write-Success "================================"
    Write-Success "   • 프로필에서 새 포스트 확인"
    Write-Success "   • 시간: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    Write-Success "================================"
    exit 0
} else {
    Write-Error_ ""
    Write-Error_ "================================"
    Write-Error_ "❌ 인스타그램 게시 실패"
    Write-Error_ "================================"
    Write-Error_ $result
    Write-Error_ "================================"
    exit 1
}
