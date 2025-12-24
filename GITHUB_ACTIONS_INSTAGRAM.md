# 🐳 GitHub Actions에서 인스타그램 자동 게시

## ✨ 개요

GitHub Actions에서 매일 자동으로 주식 브리핑을 생성하고 **Docker를 통해 인스타그램에 게시**합니다.

```
GitHub Actions (Ubuntu)
│
├─ [1] 화제 종목 조회 ✅
├─ [2] 브리핑 생성 ✅
├─ [3] 결과 GitHub에 Push ✅
│
└─ [4] 📱 Docker를 이용한 인스타그램 게시 ✅
    └─ pydantic 버전 충돌 없음 (컨테이너에 격리)
```

---

## 🚀 5분 설정 가이드

### Step 1️⃣: GitHub Secrets 설정 (2분)

GitHub 저장소에서:

1. **Settings → Secrets and variables → Actions**
2. **New repository secret** 클릭
3. 다음 2개의 secret 추가:

**Secret 1:**
```
Name: INSTAGRAM_USERNAME
Value: s4a2z7
```

**Secret 2:**
```
Name: INSTAGRAM_PASSWORD
Value: claude2022!
```

**저장 후 확인:**
```
✅ INSTAGRAM_USERNAME (마스킹됨)
✅ INSTAGRAM_PASSWORD (마스킹됨)
```

### Step 2️⃣: 워크플로우 파일 확인 (1분)

다음 파일이 이미 생성되어 있습니다:

```
.github/workflows/daily_briefing_instagram.yml
```

이 파일이 다음을 수행합니다:
- ✅ 매일 UTC 22:00 (KST 07:00)에 실행
- ✅ 화제 종목 조회
- ✅ 브리핑 생성
- ✅ 결과를 GitHub에 Push
- ✅ 📱 Docker로 인스타그램 게시

### Step 3️⃣: 배포 (즉시 테스트)

GitHub 웹사이트에서:

1. **Actions 탭** 클릭
2. **Daily Stock Briefing with Instagram Posting** 선택
3. **Run workflow** 클릭
4. **Run workflow** 확인

**약 5-10분 후:**
- ✅ 모든 단계 완료
- ✅ Instagram 프로필에 새 포스트 나타남

---

## 📊 워크플로우 흐름

### 자동 실행 (매일 07:00 AM KST)

```
타이머 (UTC 22:00)
    ↓
[Job 1: Briefing]
├─ 화제 종목 조회 (Yahoo Finance)
├─ 브리핑 생성 (텍스트 + 이미지)
└─ GitHub에 Push
    ↓
[Job 2: Instagram] (완료 대기)
├─ Docker 이미지 빌드
├─ 컨테이너 실행
└─ 📱 인스타그램 게시
    ↓
✅ 완료 (약 10-15분 소요)
```

### 수동 실행

1. GitHub → **Actions 탭**
2. **Daily Stock Briefing with Instagram Posting** 선택
3. **Run workflow** → **Run workflow**

---

## 🔐 GitHub Secrets 설정 방법 (상세)

### 방법 1: 웹사이트 (권장)

1. GitHub 저장소 열기
2. **Settings** (우측 상단)
3. **Secrets and variables** → **Actions**
4. **New repository secret** 클릭

```
Name: INSTAGRAM_USERNAME
Value: s4a2z7
```

5. **Add secret** 클릭
6. 같은 방식으로 `INSTAGRAM_PASSWORD` 추가

### 방법 2: GitHub CLI

```bash
# GitHub CLI 설치 필요
gh secret set INSTAGRAM_USERNAME --body "s4a2z7"
gh secret set INSTAGRAM_PASSWORD --body "claude2022!"
```

### 확인

```bash
gh secret list
```

출력:
```
INSTAGRAM_PASSWORD  Updated Dec 25, 2025
INSTAGRAM_USERNAME  Updated Dec 25, 2025
```

---

## 🔍 실행 확인

### 1. Actions 탭에서 확인

```
Workflow runs
├─ Daily Stock Briefing with Instagram Posting
│  ├─ ✅ briefing (7min)
│  └─ ✅ instagram (3min)
└─ Conclusion: Success
```

### 2. Instagram 프로필 확인

프로필에 다음과 같은 포스트가 나타남:

```
📈 2025년 12월 25일 주식 브리핑

🔥 거래량 많은 종목
1. NVDA $171.34 -9.44%

📈 오늘의 상승 종목
1. EWTX $22.80 +4.85%

📉 오늘의 하락 종목
1. HYMC $12.55 -53.76%

#주식 #투자 #트렌드주 #화제종목
#주식시장 #주식정보

[이미지 첨부]
```

### 3. GitHub 저장소 확인

**output/** 폴더에 다음이 자동 Push됨:

```
output/
├── data/
│   └── screener_results_20251225.json
│   └── briefings_20251225.json
├── images/
│   └── briefing_card_20251225.png
└── reports/
    └── briefing_20251225.md
```

---

## 🛠️ 문제 해결

### ❌ "Secrets not found" 오류

```
Error: INSTAGRAM_USERNAME not found in secrets
```

**해결:**
1. GitHub Settings → Secrets 다시 확인
2. 정확한 이름으로 설정되었는지 확인
3. 특수문자나 공백이 없는지 확인

### ❌ "Docker build failed"

```
ERROR: failed to solve with frontend dockerfile.v0
```

**해결:**
1. Dockerfile.instagram 파일 확인
2. Docker 이미지가 올바른지 확인
3. 로그에서 실패 원인 확인

### ❌ "Instagram posting failed"

```
❌ Instagram posting failed
```

**해결:**
1. Instagram 계정 정보 확인
2. 2단계 인증 설정 확인
3. 비밀번호 변경 후 다시 시도

### ❌ "No images found"

```
Image not found: output/images/briefing_card_*.png
```

**해결:**
1. `Generate Briefing` 단계가 성공했는지 확인
2. GitHub에 output/ 폴더가 Push되었는지 확인
3. 이미지 파일이 생성되었는지 확인

---

## 📚 파일 설명

| 파일 | 용도 |
|------|------|
| `.github/workflows/daily_briefing_instagram.yml` | 📝 GitHub Actions 워크플로우 |
| `Dockerfile.instagram` | 🐳 Docker 이미지 설정 |
| `backend/requirements_instagram.txt` | 📦 Python 의존성 |
| `backend/services/instagram_service.py` | 📱 인스타그램 서비스 |

---

## ⏰ 스케줄

### 기본 설정

```yaml
on:
  schedule:
    - cron: '0 22 * * *'  # UTC 22:00 = KST 07:00
```

### 다른 시간으로 변경

**예시: 매일 09:00 KST (UTC 00:00)**

```yaml
cron: '0 0 * * *'
```

**시간 변환:**
```
KST = UTC + 9시간

KST 07:00 → UTC 22:00 (전날)
KST 09:00 → UTC 00:00
KST 12:00 → UTC 03:00
KST 18:00 → UTC 09:00
```

---

## 🔐 보안

### ✅ 안전한 관행

1. **Secrets 사용**
   - 평문으로 저장하지 않음
   - GitHub에서 자동 마스킹됨

2. **로그 보안**
   - Secrets 값이 로그에 출력되지 않음
   - GitHub이 자동으로 필터링

3. **Docker 격리**
   - pydantic 버전 충돌 없음
   - 컨테이너에서 안전하게 실행

### ⚠️ 주의사항

- ❌ 코드에 비밀번호 입력하지 말 것
- ❌ 로그에 출력하지 말 것
- ❌ .env 파일을 GitHub에 커밋하지 말 것

---

## 🚀 고급 설정

### 실패 시 자동 재시도

```yaml
- name: Post to Instagram
  run: docker run --rm ... instagram-poster
  continue-on-error: true
```

### 특정 시간에만 실행

```yaml
- name: Post to Instagram
  if: github.event.schedule == '0 22 * * *'  # 특정 시간만
  run: docker run --rm ... instagram-poster
```

### Slack 알림 (선택)

```yaml
- name: Notify Slack
  if: success()
  run: |
    curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
      -d '{"text":"✅ Instagram posting completed!"}'
```

---

## 📞 지원

### 문제 해결

1. **Actions 로그 확인**
   - GitHub → Actions → 워크플로우 클릭
   - 각 단계의 로그 확인

2. **Docker 로그**
   - "Post to Instagram" 단계의 로그 보기
   - 오류 메시지 분석

3. **Instagram 확인**
   - 프로필에 새 포스트 있는지 확인
   - 댓글이나 좋아요 확인

---

## ✅ 체크리스트

- [ ] GitHub Secrets 설정 (INSTAGRAM_USERNAME)
- [ ] GitHub Secrets 설정 (INSTAGRAM_PASSWORD)
- [ ] `.github/workflows/daily_briefing_instagram.yml` 확인
- [ ] GitHub Actions 탭에서 "Run workflow" 실행
- [ ] 약 10-15분 후 완료 확인
- [ ] Instagram 프로필에서 새 포스트 확인
- [ ] 매일 07:00 AM (KST) 자동 실행 확인

---

## 🎉 완성!

```
✅ GitHub Actions에서 매일 자동으로:
├─ 화제 종목 조회
├─ 브리핑 생성
└─ 📱 인스타그램 게시

🌍 클라우드 기반 자동화 (별도 컴퓨터 불필요!)
```

**이제 GitHub Actions으로 완전 자동화된 인스타그램 브리핑 시스템이 준비되었습니다!** 🚀

---

## 📚 관련 문서

- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - 로컬 Docker 배포
- [DOCKER_INSTAGRAM_QUICK_START.md](DOCKER_INSTAGRAM_QUICK_START.md) - Docker 5분 가이드
- [.github/workflows/daily_briefing_instagram.yml](.github/workflows/daily_briefing_instagram.yml) - 워크플로우 파일
