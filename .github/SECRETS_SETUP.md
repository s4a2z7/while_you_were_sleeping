# GitHub Secrets 설정 체크리스트

## ✅ 필수 설정 항목

이 파일을 사용하여 GitHub Secrets를 올바르게 설정했는지 확인하세요.

### 단계별 설정

#### 1️⃣ GitHub Repository Settings 접근
```
https://github.com/YOUR_USERNAME/while-you-were-sleeping-dashboard/settings/secrets/actions
```

#### 2️⃣ 필수 Secrets 추가

| Secret Name | 값 | 설명 |
|-------------|-----|------|
| `SMTP_SERVER` | `smtp.gmail.com` | Gmail SMTP 서버 |
| `SMTP_PORT` | `587` | SMTP 포트 |
| `SENDER_EMAIL` | your-email@gmail.com | 발송자 이메일 |
| `SENDER_PASSWORD` | (앱 비밀번호) | Gmail 앱 비밀번호 |
| `RECIPIENT_EMAIL` | recipient@example.com | 수신자 이메일 |
| `EXA_API_KEY` | (선택사항) | Exa API 키 |
| `INSTAGRAM_USERNAME` | your_instagram_username | 인스타그램/Threads 계정 이름 |
| `INSTAGRAM_PASSWORD` | your_instagram_password | 인스타그램/Threads 계정 비밀번호 |

**참고**: Threads는 Instagram과 동일한 계정으로 발행됩니다.

#### 3️⃣ 각 항목 설정 방법

##### SMTP_SERVER
- 입력값: `smtp.gmail.com`
- 다른 메일 서비스 사용 시 해당 SMTP 서버로 변경

##### SMTP_PORT
- 입력값: `587`
- TLS 방식의 표준 포트

##### SENDER_EMAIL
- Gmail: `your-email@gmail.com`
- 대체 메일 서비스: 해당 이메일 주소

##### SENDER_PASSWORD (⚠️ 중요)
```
Gmail 기본 계정의 경우 앱 비밀번호 생성 필수!

1. https://myaccount.google.com 접속
2. 좌측 메뉴에서 "보안(Security)" 클릭
3. "2단계 인증" 활성화 (미활성화 시 활성화)
4. "앱 비밀번호(App passwords)" 클릭
5. 앱 선택: Mail / Windows Computer
6. 생성된 16자리 비밀번호 복사
7. GitHub Secret에 붙여넣기
```

##### RECIPIENT_EMAIL
- 브리핑을 받을 이메일 주소
- 예: `your-name@example.com`

##### EXA_API_KEY (선택사항)
- Exa API 키
- 없어도 기본 기능 동작
- 뉴스 기능을 원할 때만 설정

---

## 🔐 보안 확인 체크리스트

- [ ] 모든 Secrets이 GitHub 웹 인터페이스에만 입력됨 (코드에는 절대 입력 금지)
- [ ] Secrets 값이 코드, 로그, 문서에 노출되지 않음
- [ ] 앱 비밀번호가 아닌 일반 비밀번호를 사용하지 않음
- [ ] 정기적으로 비밀번호 변경 (월 1회 권장)

---

## 🧪 테스트

### 로컬 테스트
```bash
# 환경 변수 설정
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export SENDER_EMAIL="your-email@gmail.com"
export SENDER_PASSWORD="your-app-password"
export RECIPIENT_EMAIL="recipient@example.com"

# 이메일 서비스 테스트
cd backend
python -m services.email_service
```

### GitHub Actions 테스트
1. GitHub Repository > Actions 탭
2. "Daily Stock Briefing" 선택
3. "Run workflow" 버튼 클릭
4. 로그에서 "✅ 이메일 발송 성공" 확인

---

## 🆘 문제 해결

### Secrets이 설정되었는데도 작동하지 않음
1. GitHub Actions 로그에서 정확한 에러 메시지 확인
2. Secret 이름이 워크플로우 파일의 `${{ secrets.SECRET_NAME }}`과 일치하는지 확인
3. Secret 값에 공백이 있는지 확인 (있으면 제거)

### SMTP 인증 실패
```
Error: (535, b'5.7.8 Username and Password not accepted')
```
- Gmail: 앱 비밀번호 사용 확인 (일반 비밀번호 사용 불가)
- 2단계 인증 활성화 확인
- 발신 차단 해제: https://myaccount.google.com/lesssecureapps

### 이메일이 수신되지 않음
1. 스팸 폴더 확인
2. 이메일 발송 로그에서 "✅ 이메일 발송 성공" 메시지 확인
3. RECIPIENT_EMAIL이 올바른지 확인

---

## 📋 설정 완료 체크리스트

```
□ SMTP_SERVER = smtp.gmail.com
□ SMTP_PORT = 587
□ SENDER_EMAIL = (입력함)
□ SENDER_PASSWORD = (앱 비밀번호로 입력함)
□ RECIPIENT_EMAIL = (입력함)
□ EXA_API_KEY = (선택) (입력함 또는 스킵)

□ 로컬 테스트 성공
□ GitHub Actions 수동 실행 성공
□ 이메일 수신 확인
□ 마크다운 파일 첨부 확인
```

---

## 📞 추가 지원

- [GitHub Secrets 공식 문서](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)
- [Gmail 앱 비밀번호](https://support.google.com/accounts/answer/185833)
- [GitHub Actions 공식 문서](https://docs.github.com/en/actions)

---

**설정 완료 후 `daily_briefing.yml` 워크플로우가 매일 자동으로 실행됩니다!**
