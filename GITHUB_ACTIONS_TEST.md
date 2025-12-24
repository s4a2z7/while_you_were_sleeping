# 🚀 GitHub Actions 인스타그램 포스팅 테스트 가이드

## 지금 바로 테스트하는 방법 (5분)

### Step 1: GitHub Secrets 설정 확인 (필수!)

이미 설정했다면 Step 2로 넘어가세요.

**아직 안 했다면:**

1. GitHub 저장소 열기: https://github.com/YOUR_USERNAME/while-you-were-sleeping-dashboard
2. **Settings** → **Secrets and variables** → **Actions**
3. 다음 2개의 Secret이 있는지 확인:
   - ✅ `INSTAGRAM_USERNAME` = `s4a2z7`
   - ✅ `INSTAGRAM_PASSWORD` = `claude2022!`

없으면 **New repository secret** 클릭해서 추가하세요.

---

### Step 2: GitHub Actions 실행 (1분)

1. GitHub 저장소의 **Actions** 탭 클릭
2. 왼쪽 메뉴에서 **"Daily Stock Briefing with Instagram Posting"** 선택
3. 오른쪽에 **"Run workflow"** 버튼이 보임
4. **"Run workflow"** 클릭
5. 확인 팝업에서 다시 **"Run workflow"** 클릭

**상태 표시:**
```
⏳ Queued
  ↓
🔵 In progress
  ├─ ✅ briefing (2-3분)
  └─ ✅ instagram (2-3분)
  ↓
✅ Completed (약 5-10분 소요)
```

---

### Step 3: 실행 진행 상황 확인 (실시간)

**Actions 탭에서:**

1. 가장 최신 워크플로우 실행 클릭
2. 다음 단계들이 순서대로 진행되는 것 확인:

#### Job 1: Briefing (데이터 수집)
```
✅ Checkout
✅ Set up Python
✅ Install dependencies
✅ Get Trending Stocks (화제 종목 조회)
✅ Generate Briefing (브리핑 생성)
✅ Push results to repository (결과 커밋)
```

#### Job 2: Instagram (포스팅)
```
✅ Build Docker image (Docker 빌드)
✅ Push to Instagram (인스타그램 게시)
```

---

### Step 4: 결과 확인 (완료 후)

#### ✅ Instagram 프로필 확인
- https://instagram.com/s4a2z7
- 새로운 포스트가 나타나야 함

#### ✅ GitHub Repository 확인
- **output/images/** 폴더에 새 이미지
- **output/data/** 폴더에 새 JSON 데이터
- **output/reports/** 폴더에 새 리포트

#### ✅ GitHub Actions 로그 확인
- 각 단계의 상세 로그 확인 가능
- 오류가 있으면 빨간색으로 표시됨

---

## 🔍 로그 해석

### 성공한 경우 ✅

```
✅ Get Trending Stocks
📊 Most Active: NVDA, EWTX, HYMC
⏱️  Duration: 13s

✅ Generate Briefing
📸 Generated: briefing_card_20251225.png
⏱️  Duration: 40s

✅ Push to Repository
📦 Files updated: 5
🔄 Commit: [auto] Daily briefing update

✅ Build Docker image
🐳 Image: instagram-poster:latest
⏱️  Build time: 30s

✅ Post to Instagram
📱 Posted: briefing_card_20251225.png
✓ Caption added
✓ Image uploaded
⏱️  Duration: 5s
```

### 실패한 경우 ❌

**Error: Secrets not found**
```
→ Solution: GitHub Settings → Secrets 다시 확인
→ INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD 설정 확인
```

**Error: Docker build failed**
```
→ Solution: Dockerfile.instagram 파일 확인
→ 파일이 .github/workflows/ 폴더와 같은 레벨에 있는지 확인
```

**Error: Instagram posting failed**
```
→ Solution: 비밀번호 확인
→ Instagram 2단계 인증 설정 확인
→ IP 차단 여부 확인 (Instagram에 로그인해서 보안 확인)
```

**Error: Image not found**
```
→ Solution: Briefing 생성 단계가 성공했는지 확인
→ output/images/ 폴더에 briefing_card_*.png가 있는지 확인
```

---

## ⏱️ 예상 소요 시간

| 단계 | 소요 시간 |
|------|----------|
| 큐 대기 | 1-3초 |
| Python 설정 | 15-30초 |
| 의존성 설치 | 30-60초 |
| 화제 종목 조회 | 15-30초 |
| 브리핑 생성 | 40-60초 |
| GitHub 커밋 | 5-10초 |
| Docker 빌드 | 20-40초 |
| Instagram 포스팅 | 3-10초 |
| **총 예상 시간** | **5-10분** |

---

## 🎯 정확한 클릭 경로

### 웹사이트에서 직접 실행

```
1️⃣  GitHub 저장소 열기
   ↓
2️⃣  "Actions" 탭 클릭
   ↓
3️⃣  왼쪽 메뉴에서 "Daily Stock Briefing with Instagram Posting" 선택
   ↓
4️⃣  "Run workflow" 버튼 클릭 (오른쪽 상단)
   ↓
5️⃣  "Run workflow" 확인 클릭
   ↓
6️⃣  대기... (5-10분)
   ↓
7️⃣  ✅ 완료!
   ↓
8️⃣  @s4a2z7 Instagram 프로필 확인
```

---

## 📋 체크리스트

테스트 전에 확인:

- [ ] GitHub Secrets 설정 (INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
- [ ] 저장소에 `.github/workflows/daily_briefing_instagram.yml` 파일 있음
- [ ] `Dockerfile.instagram` 파일 있음
- [ ] `backend/services/instagram_service.py` 파일 있음
- [ ] `backend/services/screener_service.py` 파일 있음
- [ ] `backend/services/briefing_generator.py` 파일 있음

---

## 🆘 트러블슈팅

### "Run workflow" 버튼이 안 보임

❌ 원인: `workflow_dispatch` 미설정
✅ 해결:
```yaml
on:
  schedule:
    - cron: '0 22 * * *'
  workflow_dispatch:  # 이 줄이 있어야 함
```

### Secrets가 안 적용됨

❌ 원인: Secrets 이름이 다름
✅ 확인: 정확히 이 이름으로 설정되었는지 확인
- `INSTAGRAM_USERNAME` (스페이스 없음, 모두 대문자)
- `INSTAGRAM_PASSWORD` (스페이스 없음, 모두 대문자)

### 이미지가 생성되지 않음

❌ 원인: Python 의존성 부족
✅ 해결: `requirements.txt`에 다음이 있는지 확인
```
pillow>=9.0.0
```

### Docker 빌드 실패

❌ 원인: `Dockerfile.instagram` 경로 오류
✅ 확인: 파일이 저장소 루트에 있는지 확인
```
while-you-were-sleeping-dashboard/
├── Dockerfile.instagram (← 여기)
├── .github/
│   └── workflows/
│       └── daily_briefing_instagram.yml
└── backend/
```

---

## 💡 팁

### 빠르게 테스트하기
1. Actions 탭에서 "Run workflow" 클릭
2. 동시에 Instagram 프로필 열어놓기
3. 5분 후 새로고침

### 로그 확인하기
1. 실행 중인 Job 클릭
2. 오른쪽의 스텝 이름 클릭
3. 상세 로그 확인

### 오류 디버깅하기
1. 실패한 스텝 확인
2. 빨간색 오류 메시지 읽기
3. 위의 트러블슈팅 참조

---

## 🎉 성공 신호

모든 게 제대로 되면:

```
✅ GitHub Actions 워크플로우 완료
✅ Instagram에 새 포스트 나타남
✅ 포스트에 매일의 주식 정보 포함
✅ 이미지와 캡션 정상 표시
✅ GitHub Repository 업데이트됨
```

**축하합니다!** 🎊 이제 매일 자동으로 인스타그램에 주식 브리핑이 게시됩니다!

---

## 🔄 다음 단계

### 일주일 후 확인
- 매일 07:00 AM (KST)에 자동 실행되는지 확인
- 인스타그램 포스트가 매일 1개씩 추가되는지 확인
- 오류가 없는지 확인

### 문제 발견 시
- GitHub Actions 로그 확인
- 위의 트러블슈팅 참조
- 필요하면 Settings → Secrets 업데이트

### 추가 최적화
- 포스팅 시간 변경하기 (cron 표현식 수정)
- 캡션 포맷 변경하기
- 이미지 디자인 수정하기

---

## 📞 도움말

**자주 묻는 질문:**

**Q: 지금 바로 테스트할 수 있나요?**
A: 네! "Run workflow" 버튼으로 언제든 테스트 가능합니다.

**Q: 실패하면 다시 할 수 있나요?**
A: 네! 몇 번이든 다시 실행해도 괜찮습니다.

**Q: 얼마나 자주 포스팅되나요?**
A: 매일 07:00 AM (KST, UTC 22:00 전날)에 자동 포스팅됩니다.

**Q: Instagram 팔로워들에게 보일까요?**
A: 네! 정상적으로 포스팅되면 피드에 나타납니다.

---

**지금 바로 시작해보세요!** 🚀
