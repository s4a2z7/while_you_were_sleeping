# Meta Graph API로 Instagram 자동 포스팅

## 📋 사전 준비 (10분)

### 1️⃣ Meta Developer 계정 생성

1. https://developers.facebook.com 접속
2. **내 앱** → **앱 만들기**
3. 앱 유형: **비즈니스** 선택
4. 앱 이름: `While You Were Sleeping` 입력

### 2️⃣ Instagram Graph API 설정

1. 앱 대시보드 → **제품** → **추가**
2. **Instagram Graph API** 검색 → **설정**
3. **Instagram Basic Display** 추가

### 3️⃣ Business Account 연결

1. 설정 → **기본 설정**
2. **앱 도메인**: `localhost` 입력
3. 계속 진행

### 4️⃣ Access Token 생성

1. 도구 → **Graph API Explorer**
2. 앱 선택: 방금 만든 앱
3. 액세스 유형: **앱 토큰** 선택
4. 권한: 다음 권한 확인
   ```
   instagram_business_basic
   instagram_business_content_publish
   pages_read_user_content
   ```
5. **토큰 생성** 클릭
6. 생성된 긴 문자열 복사 → `.env`에 저장

### 5️⃣ Instagram Business Account ID 찾기

1. Graph API Explorer에서 쿼리 실행:
   ```
   GET /me/instagram_business_accounts
   ```
2. 응답에서 `id` 값 복사
3. `.env`에 저장

## 🔧 설정 파일 (`backend/.env`)

다음을 추가하세요:

```env
# Meta Graph API
META_ACCESS_TOKEN=your_access_token_here
META_INSTAGRAM_BUSINESS_ACCOUNT_ID=your_business_account_id_here
META_INSTAGRAM_BUSINESS_PAGE_ID=your_page_id_here
```

### 토큰 어디서 얻는지:

**Access Token 가져오기:**
1. https://developers.facebook.com/tools/explorer
2. 앱 선택
3. 토큰 생성 → 복사

**Business Account ID 가져오기:**
1. 같은 Graph API Explorer에서:
   ```
   GET /me/instagram_business_accounts
   ```
2. 응답의 `id` 복사

**Page ID 가져오기:**
1. Graph API Explorer에서:
   ```
   GET /me/accounts
   ```
2. Instagram 연결된 페이지의 `id` 복사

## ✅ 검증

설정 후 이 명령어 실행:

```bash
cd backend
python -m services.meta_instagram_service
```

정상 작동 시:
```
✅ Meta Instagram 클라이언트 초기화 완료
✅ Meta Instagram 로그인 성공
✅ Meta Instagram 포스팅 완료
```

## 🎯 이점

- ✅ **안정적**: Meta 공식 API
- ✅ **빠름**: IP 차단 없음
- ✅ **신뢰성**: 장기 지원
- ✅ **GitHub Actions 호환**: 클라우드에서도 작동

## ⚠️ 주의사항

1. **Business Account 필요**
   - 개인 계정이 아닌 Business 계정이어야 함
   - 개인 계정 → Business로 전환 가능

2. **토큰 보안**
   - Access Token을 공개하지 마세요
   - `.env` 파일을 `.gitignore`에 포함 (이미 포함됨)

3. **Rate Limit**
   - 시간당 200개 요청 제한
   - 우리는 하루 1개만 포스팅하므로 무관

## 🆘 문제 해결

**"Invalid access token" 오류**
- Access Token 확인
- 토큰 갱신 필요 (60일마다)

**"Invalid IG User ID" 오류**
- Business Account ID 확인
- 올바른 형식: 숫자만 포함

**권한 오류**
- 앱 권한 재확인
- `instagram_business_content_publish` 추가 필요

## 📞 도움말

Meta Developer 문서:
https://developers.facebook.com/docs/instagram-api/reference/ig-media#create

질문이 있으면 GitHub Issues에 남겨주세요!
