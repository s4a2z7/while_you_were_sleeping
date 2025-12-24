# Windows Task Scheduler 자동화 설정 가이드

## 📋 설정 방법

### Step 1: Python 경로 확인
```powershell
python -c "import sys; print(sys.executable)"
```
예시: `C:\Users\LG\AppData\Local\Programs\Python\Python312\python.exe`

### Step 2: Task Scheduler 열기
```
Windows + R → taskschd.msc
```

### Step 3: 새 작업 생성
1. 우측 패널에서 "작업 만들기" 클릭
2. 이름: `Daily Stock Briefing`
3. "최상의 권한으로 실행" 체크

### Step 4: 트리거 설정 (Triggers 탭)
- "새로 만들기" 클릭
- 트리거 유형: "일정에 따라"
- 매일 오전 7:00 AM 설정
- 반복: 매일

### Step 5: 작업 설정 (Actions 탭)
1. "새로 만들기" 클릭
2. **작업**: `프로그램 시작`
3. **프로그램/스크립트**:
```
C:\Users\LG\AppData\Local\Programs\Python\Python312\python.exe
```
(위에서 확인한 Python 경로로 변경)

4. **인수 추가**:
```
"C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\run_daily_briefing.py"
```

5. **시작 위치**:
```
C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard
```

### Step 6: 조건 설정 (Conditions 탭)
- "컴퓨터가 AC 전원에 연결되어 있어야 함" 체크 해제
- "유휴 상태일 필요는 없음" 체크

### Step 7: 설정 (Settings 탭)
- "작업이 실패하면 다시 실행" 체크
- 다시 시도 간격: 5분
- 재시도 횟수: 3회

### Step 8: 확인 및 저장
- 확인 클릭
- 암호 입력 (Windows 로그인 암호)

## ✅ 테스트

Task Scheduler에서 작업을 우클릭 → "실행"

로그 파일 확인:
```powershell
Get-Content "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\briefing_scheduler.log" -Tail 20
```

## 📊 일정

매일 오전 7:00 AM에 자동 실행됨
- Screener: 화제 종목 수집
- Generator: 브리핑 생성
- Email: 이메일 발송

## 🔧 문제 해결

**로그 파일 위치**:
```
C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\briefing_scheduler.log
```

**이메일이 안 오면**:
1. `.env` 파일의 Gmail 자격증명 확인
2. 앱 비밀번호 (16자리) 확인
3. `python test_email_setup.py` 로컬 테스트

**Task Scheduler 로그**:
- 실행 기록 → 작업 스케줄러 라이브러리
- Daily Stock Briefing 작업의 상태 확인

## 💡 GitHub Actions와의 차이

| 기능 | GitHub Actions | Local Task Scheduler |
|------|---|---|
| 외부 SMTP | ❌ 차단됨 | ✅ 작동 |
| 이메일 발송 | ❌ 불가능 | ✅ 가능 |
| 스케줄 | ✅ cron 지원 | ✅ Task Scheduler |
| 비용 | ✅ 무료 | ✅ 무료 |
| 항상 실행 | ✅ GitHub 서버 | ❌ 컴퓨터 켜야 함 |

## 📝 참고

GitHub Actions는 여전히 작동하며:
- ✅ 화제 종목 조회
- ✅ 브리핑 생성
- ✅ GitHub에 자동 커밋 (선택사항)

로컬 Task Scheduler는:
- ✅ 위의 모든 기능
- ✅ 이메일 발송
- ✅ 로컬 파일 저장
