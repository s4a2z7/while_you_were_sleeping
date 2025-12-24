@echo off
REM ================================================
REM Instagram 포스팅 자동화 (Windows Task Scheduler)
REM ================================================
REM 실행 시간: 매일 07:10 AM (GitHub Actions가 07:00에 데이터 생성 후)
REM 용도: 생성된 브리핑 이미지를 Instagram에 포스팅

setlocal enabledelayedexpansion

REM 기본 설정
set SCRIPT_DIR=%~dp0
set BACKEND_DIR=%SCRIPT_DIR%backend
set LOG_DIR=%SCRIPT_DIR%logs
set LOG_FILE=%LOG_DIR%\instagram_posting.log

REM 로그 폴더 생성
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM 타임스탬프
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a:%%b)

echo. >> "%LOG_FILE%"
echo ================================================ >> "%LOG_FILE%"
echo [%mydate% %mytime%] Instagram 포스팅 시작 >> "%LOG_FILE%"
echo ================================================ >> "%LOG_FILE%"

REM Python 실행
cd /d "%BACKEND_DIR%"

echo [%mydate% %mytime%] Python 인스타그램 서비스 실행 중... >> "%LOG_FILE%"
python -m services.instagram_service >> "%LOG_FILE%" 2>&1

if %ERRORLEVEL% equ 0 (
    echo [%mydate% %mytime%] ✅ 인스타그램 포스팅 완료 >> "%LOG_FILE%"
) else (
    echo [%mydate% %mytime%] ❌ 인스타그램 포스팅 실패 >> "%LOG_FILE%"
)

echo [%mydate% %mytime%] 작업 종료 >> "%LOG_FILE%"

endlocal
