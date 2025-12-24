# ⚡ 관리자 권한으로 실행하는 방법

## 🔴 오류: 액세스가 거부되었습니다 (Permission Denied)

Windows Task Scheduler에 작업을 등록하려면 **관리자 권한**이 필수입니다.

---

## ✅ 해결 방법

### **방법 1: PowerShell을 관리자로 재시작 (권장)**

1. **Windows + R** 눌러서 실행창 열기
2. `powershell` 입력
3. **Ctrl + Shift + Enter** 눌러서 관리자 권한으로 실행
   - 또는 우클릭 → "관리자 권한으로 실행"
4. 다음 명령 실행:

```powershell
cd "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard"
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
.\setup_task_scheduler.ps1
```

---

### **방법 2: 수동으로 Task Scheduler에 작업 등록**

#### Step 1: Task Scheduler 열기
```
Windows + R → taskschd.msc → Enter
```

#### Step 2: 작업 만들기
```
좌측 패널 → "작업 만들기"
```

#### Step 3: 일반 탭
```
이름: Daily Stock Briefing
☑ 최상의 권한으로 실행 (반드시 체크!)
```

#### Step 4: 트리거 탭
```
"새로 만들기" →
- 트리거 유형: 일정에 따라
- 매일
- 시간: 07:00
- "확인"
```

#### Step 5: 작업 탭
```
"새로 만들기" →
- 프로그램/스크립트:
  C:\Users\LG\AppData\Local\Programs\Python\Python312\python.exe
  (또는 python -c "import sys; print(sys.executable)" 로 확인)
  
- 인수 추가:
  C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\run_daily_briefing.py
  
- 시작 위치:
  C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard
  
- "확인"
```

#### Step 6: 조건 탭
```
☐ 컴퓨터가 AC 전원에 연결되어 있어야 함
☐ 유휴 상태일 필요는 없음
☑ 네트워크 사용 가능한 경우에만 시작 (체크)
```

#### Step 7: 설정 탭
```
☑ 작업이 실패하면 다시 시도
- 다시 시도 간격: 5분
- 재시도 횟수: 3회
- "확인"
```

#### Step 8: 확인
```
"확인" 클릭
Windows 비밀번호 입력 (있는 경우)
```

---

## ✨ 완료!

이제 **매일 오전 7:00 AM에** 다음이 자동 실행됩니다:

1. ✅ 화제 종목 조회 (Yahoo Finance)
2. ✅ 브리핑 생성 (텍스트 + 이미지)
3. ✅ 이메일 발송 (Gmail)
4. ✅ 로그 저장

---

## 🔍 확인 방법

### 작업이 등록되었는지 확인
```powershell
Get-ScheduledTask -TaskName "Daily Stock Briefing"
```

### 로그 파일 보기
```powershell
Get-Content "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\briefing_scheduler.log" -Tail 30
```

### 실시간 모니터링
```powershell
Get-Content "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\briefing_scheduler.log" -Wait
```

---

## 📝 수동 테스트

Task Scheduler에서 작업을 바로 실행해보세요:

1. **Windows + R** → `taskschd.msc` → Enter
2. **Daily Stock Briefing** 찾기
3. 우클릭 → **실행**
4. 1-2분 기다린 후 이메일 확인

---

**문제가 있으면 다음을 확인하세요:**

- ✅ Python 설치 확인: `python --version`
- ✅ 스크립트 경로: `C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\run_daily_briefing.py`
- ✅ .env 파일 설정: `backend/.env` (Gmail 자격증명)
- ✅ 로그 파일: `briefing_scheduler.log` (오류 메시지 확인)
