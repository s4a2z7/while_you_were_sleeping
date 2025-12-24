# 🚀 Windows Task Scheduler 빠른 설정 가이드

## ⚡ 자동 설정 (3단계)

### Step 1: PowerShell을 **관리자 권한**으로 열기

```powershell
# Windows + X → Windows PowerShell (관리자)
# 또는
# Windows 시작 → "powershell" 검색 → 우클릭 → "관리자 권한으로 실행"
```

### Step 2: 보안 정책 임시 변경 (일회성)

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
```

### Step 3: 설정 스크립트 실행

```powershell
cd "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard"
.\setup_task_scheduler.ps1
```

✅ 완료! 매일 오전 7:00 AM에 자동 실행됩니다.

---

## 📋 수동 설정 (상세 가이드)

원한다면 다음 단계로 수동 설정도 가능합니다:

### 1. Task Scheduler 열기
```
Windows + R → taskschd.msc → Enter
```

### 2. 새 작업 만들기
```
우측 패널 → "작업 만들기"
```

### 3. 작업 탭 설정
```
이름: Daily Stock Briefing
□ 최상의 권한으로 실행 (체크)
```

### 4. 트리거 탭 설정
```
"새로 만들기" → 
- 트리거 유형: 일정에 따라
- 매일
- 07:00 (오전 7시)
```

### 5. 작업 탭 설정
```
"새로 만들기" →
- 프로그램/스크립트: C:\Users\LG\AppData\Local\Programs\Python\Python312\python.exe
  (python -c "import sys; print(sys.executable)" 명령으로 확인)
- 인수 추가: "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\run_daily_briefing.py"
- 시작 위치: C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard
```

### 6. 조건 탭 설정
```
☐ 컴퓨터가 AC 전원에 연결되어 있어야 함 (체크 해제)
☐ 유휴 상태일 필요는 없음 (체크 해제)
```

### 7. 설정 탭 설정
```
☑ 작업이 실패하면 다시 시도
- 다시 시도 간격: 5분
- 재시도 횟수: 3회
```

### 8. 확인 및 저장
```
확인 버튼 클릭
Windows 암호 입력
```

---

## ✅ 테스트 및 확인

### 1. 작업 확인
```powershell
Get-ScheduledTask -TaskName "Daily Stock Briefing"
```

### 2. 수동 실행 (한 번 테스트)
```
Task Scheduler → Daily Stock Briefing 우클릭 → 실행
```

### 3. 로그 확인
```powershell
Get-Content "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\briefing_scheduler.log" -Tail 30
```

### 4. 실시간 모니터링
```powershell
Get-Content "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\briefing_scheduler.log" -Wait
```

---

## 🔧 관리 및 문제 해결

### 작업 비활성화
```powershell
Disable-ScheduledTask -TaskName "Daily Stock Briefing"
```

### 작업 재활성화
```powershell
Enable-ScheduledTask -TaskName "Daily Stock Briefing"
```

### 작업 삭제
```powershell
Unregister-ScheduledTask -TaskName "Daily Stock Briefing" -Confirm:$false
```

### 로그 파일 지우기
```powershell
Clear-Content "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\briefing_scheduler.log"
```

---

## 🔍 이메일이 안 오면?

### 1. .env 파일 확인
```powershell
cd "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\backend"
cat .env
```

필수 설정:
```
SENDER_EMAIL=chocomadeline70@gmail.com
SENDER_PASSWORD=aktfmrnnrzpjfbke  # 16자리 앱 비밀번호
RECIPIENT_EMAIL=chocomadeline70@gmail.com
```

### 2. 로컬 테스트
```powershell
cd "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\backend"
python test_email_setup.py
```

### 3. 로그 파일 확인
```powershell
Get-Content "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\briefing_scheduler.log" -Tail 50
```

---

## 📊 동작 확인

매일 오전 7:00에:
1. ✅ 화제 종목 조회 (Yahoo Finance)
2. ✅ 브리핑 생성 (텍스트, 이미지)
3. ✅ 이메일 발송 (Gmail)
4. ✅ 로그 저장

파일 위치:
```
output/data/screener_results_YYYYMMDD.json  # 화제 종목
output/data/briefings_YYYYMMDD.json          # 브리핑 데이터
output/reports/briefing_YYYYMMDD.md          # 마크다운 리포트
output/images/                               # 그래프 이미지
briefing_scheduler.log                       # 실행 로그
```

---

## 💡 추가 팁

### Outlook에서 Gmail 추가하려면?
```
1. Outlook 열기
2. 파일 → 계정 추가
3. Gmail 계정 입력
4. 2단계 인증 후 앱 비밀번호 입력
```

### 다른 시간에 실행하려면?
```powershell
# Task Scheduler에서 작업 우클릭 → 속성
# 트리거 탭 → 기존 트리거 수정 → 시간 변경
```

### 매주 특정 요일에만 실행하려면?
```powershell
# Task Scheduler에서 작업 우클릭 → 속성
# 트리거 탭 → 기존 트리거 수정
# "매주"로 변경 후 요일 선택
```

---

**이제 준비 완료! 자동화된 주식 브리핑을 받으세요! 📧**
