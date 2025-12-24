"""
이메일 발송 서비스
생성된 브리핑을 이메일로 발송하는 스크립트
"""

import asyncio
import logging
from datetime import datetime
from pathlib import Path
import json
import smtplib
import socket
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import sys
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 부모 디렉토리를 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

# 로거 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EmailService:
    """이메일 발송 서비스"""
    
    def __init__(self):
        """이메일 서비스 초기화"""
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        
        # SMTP_PORT 안전하게 처리
        smtp_port_str = os.getenv("SMTP_PORT", "587")
        try:
            self.smtp_port = int(smtp_port_str) if smtp_port_str else 587
        except (ValueError, TypeError):
            self.smtp_port = 587
            logger.warning(f"⚠️ 유효하지 않은 SMTP_PORT: {smtp_port_str}, 기본값 587 사용")
        
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        self.recipient_email = os.getenv("RECIPIENT_EMAIL")
        
        # 상세 디버깅 로그
        logger.info("=" * 60)
        logger.info("📧 이메일 서비스 설정 상태:")
        logger.info(f"   SMTP_SERVER: {self.smtp_server}")
        logger.info(f"   SMTP_PORT: {self.smtp_port}")
        logger.info(f"   SENDER_EMAIL: {'✓ 설정됨' if self.sender_email else '✗ 미설정'}")
        logger.info(f"   SENDER_PASSWORD: {'✓ 설정됨' if self.sender_password else '✗ 미설정'}")
        logger.info(f"   RECIPIENT_EMAIL: {'✓ 설정됨' if self.recipient_email else '✗ 미설정'}")
        logger.info("=" * 60)
        
        # 필수 환경 변수 확인
        if not all([self.sender_email, self.sender_password, self.recipient_email]):
            logger.error("❌ 필수 이메일 설정이 누락되었습니다!")
            logger.error("   필요한 환경 변수:")
            logger.error("   - SENDER_EMAIL")
            logger.error("   - SENDER_PASSWORD (Gmail 앱 비밀번호)")
            logger.error("   - RECIPIENT_EMAIL")
    
    def send_briefing_email(self, briefings: dict, markdown_file: Path = None) -> bool:
        """
        브리핑을 이메일로 발송
        
        Args:
            briefings: 브리핑 데이터 딕셔너리
            markdown_file: 마크다운 파일 경로 (첨부 파일)
        
        Returns:
            발송 성공 여부
        """
        try:
            logger.info("=" * 60)
            logger.info("📧 이메일 발송 준비 중...")
            
            # 필수 설정 확인
            if not self.sender_email:
                logger.error("❌ SENDER_EMAIL이 설정되지 않았습니다.")
                logger.error("   GitHub Secrets 확인: Repository → Settings → Secrets → SENDER_EMAIL")
                return False
            
            if not self.sender_password:
                logger.error("❌ SENDER_PASSWORD(앱 비밀번호)이 설정되지 않았습니다.")
                logger.error("   Gmail 앱 비밀번호 생성: https://myaccount.google.com")
                return False
            
            if not self.recipient_email:
                logger.error("❌ RECIPIENT_EMAIL이 설정되지 않았습니다.")
                return False
            
            logger.info(f"✓ 발신자: {self.sender_email}")
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"당신이 잠든 사이 - 일일 주식 브리핑 ({datetime.now().strftime('%Y년 %m월 %d일')})"
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            
            # HTML 콘텐츠 작성
            html_content = self._create_html_content(briefings)
            
            # 텍스트 버전
            text_part = MIMEText("본 이메일은 HTML 형식으로 작성되었습니다.", 'plain', _charset='utf-8')
            
            # HTML 버전
            html_part = MIMEText(html_content, 'html', _charset='utf-8')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            # 마크다운 파일 첨부
            if markdown_file and markdown_file.exists():
                try:
                    with open(markdown_file, 'rb') as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                    
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename= {markdown_file.name}')
                    msg.attach(part)
                    logger.info(f"   ✓ 첨부 파일: {markdown_file.name}")
                except Exception as e:
                    logger.warning(f"   ⚠️ 첨부 파일 추가 실패: {e}")
            
            # SMTP 연결 시도 (재시도 로직 포함)
            logger.info(f"📡 SMTP 서버 연결 시도: {self.smtp_server}:{self.smtp_port}...")
            
            max_retries = 3
            for attempt in range(1, max_retries + 1):
                try:
                    # 타임아웃을 30초로 증가
                    with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=30) as server:
                        logger.info(f"   ✓ SMTP 서버 연결 성공 (시도 {attempt}/{max_retries})")
                        
                        # TLS 시작
                        logger.info("   🔒 TLS 암호화 시작...")
                        server.starttls()
                        logger.info("   ✓ TLS 활성화 완료")
                        
                        # 로그인
                        logger.info("   🔐 Gmail 인증 중...")
                        server.login(self.sender_email, self.sender_password)
                        logger.info("   ✓ 인증 성공")
                        
                        # 발송
                        logger.info("   📤 이메일 발송 중...")
                        server.send_message(msg)
                        logger.info("   ✓ 이메일 발송 완료")
                    
                    logger.info("=" * 60)
                    logger.info("✅ 이메일 발송 성공")
                    logger.info("=" * 60)
                    return True
                    
                except (socket.gaierror, socket.timeout) as e:
                    if attempt < max_retries:
                        logger.warning(f"   ⚠️ 연결 실패 (시도 {attempt}/{max_retries}): {str(e)}")
                        logger.warning(f"   🔄 5초 후 재시도...")
                        time.sleep(5)
                        continue
                    else:
                        raise
                        
                except smtplib.SMTPAuthenticationError as e:
                    logger.error("❌ SMTP 인증 실패")
                    logger.error(f"   원인: {str(e)}")
                    logger.error("   확인사항:")
                    logger.error("   1. Gmail 주소가 정확한가?")
                    logger.error("   2. 앱 비밀번호가 올바른가? (16자리)")
                    logger.error("   3. 2단계 인증이 활성화되어 있는가?")
                    logger.error("   4. 앱 비밀번호를 최근에 생성했는가?")
                    return False
                    
                except smtplib.SMTPException as e:
                    logger.error(f"❌ SMTP 오류: {str(e)}")
                    logger.error("   SMTP 서버 설정 확인: smtp.gmail.com:587")
                    return False
            
        except socket.gaierror as e:
            logger.error(f"❌ DNS 오류: {str(e)}")
            logger.error("   SMTP 호스트를 찾을 수 없습니다.")
            logger.error("   GitHub Actions 네트워크 설정 문제일 수 있습니다.")
            return False
            
        except socket.timeout as e:
            logger.error(f"❌ 연결 타임아웃: {str(e)}")
            logger.error("   SMTP 서버 응답 시간 초과")
            return False
                logger.error("❌ SMTP 인증 실패")
                logger.error(f"   원인: {str(e)}")
                logger.error("   확인사항:")
                logger.error("   1. Gmail 주소가 정확한가?")
                logger.error("   2. 앱 비밀번호가 올바른가? (16자리)")
                logger.error("   3. 2단계 인증이 활성화되어 있는가?")
                logger.error("   4. 앱 비밀번호를 최근에 생성했는가?")
                return False
                
            except smtplib.SMTPException as e:
                logger.error(f"❌ SMTP 오류: {str(e)}")
                logger.error("   SMTP 서버 설정 확인: smtp.gmail.com:587")
                return False
            except smtplib.SMTPException as e:
                logger.error(f"❌ SMTP 오류: {str(e)}")
                logger.error("   SMTP 서버 설정 확인: smtp.gmail.com:587")
                return False
                
        except socket.gaierror as e:
            logger.error(f"❌ DNS 오류: {str(e)}")
            logger.error("   SMTP 호스트를 찾을 수 없습니다.")
            logger.error("   GitHub Actions 네트워크 설정 문제일 수 있습니다.")
            return False
            
        except socket.timeout as e:
            logger.error(f"❌ 연결 타임아웃: {str(e)}")
            logger.error("   SMTP 서버 응답 시간 초과")
            return False
            
        except Exception as e:
            logger.error(f"❌ 예기치 않은 오류: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    def _create_html_content(self, briefings: dict) -> str:
        """
        HTML 이메일 콘텐츠 생성
        
        Args:
            briefings: 브리핑 데이터
        
        Returns:
            HTML 문자열
        """
        html = f"""
        <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        background-color: #f5f5f5;
                    }}
                    .container {{
                        max-width: 800px;
                        margin: 0 auto;
                        background-color: white;
                        padding: 40px;
                        border-radius: 8px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    }}
                    .header {{
                        border-bottom: 3px solid #0066cc;
                        padding-bottom: 20px;
                        margin-bottom: 30px;
                    }}
                    .header h1 {{
                        margin: 0;
                        color: #0066cc;
                        font-size: 28px;
                    }}
                    .date {{
                        color: #666;
                        font-size: 14px;
                        margin-top: 5px;
                    }}
                    .section {{
                        margin-bottom: 30px;
                        padding: 20px;
                        background-color: #f9f9f9;
                        border-left: 4px solid #0066cc;
                        border-radius: 4px;
                    }}
                    .section h2 {{
                        margin-top: 0;
                        color: #0066cc;
                        font-size: 20px;
                    }}
                    .stock-info {{
                        background: white;
                        padding: 15px;
                        margin: 10px 0;
                        border-radius: 4px;
                    }}
                    .ticker {{
                        font-weight: bold;
                        color: #0066cc;
                        font-size: 18px;
                    }}
                    .price {{
                        font-size: 16px;
                        margin: 5px 0;
                    }}
                    .positive {{
                        color: #28a745;
                    }}
                    .negative {{
                        color: #dc3545;
                    }}
                    .footer {{
                        border-top: 1px solid #ddd;
                        padding-top: 20px;
                        margin-top: 30px;
                        font-size: 12px;
                        color: #666;
                        text-align: center;
                    }}
                    .no-data {{
                        color: #999;
                        font-style: italic;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>📈 당신이 잠든 사이</h1>
                        <p class="date">일일 주식 브리핑 - {datetime.now().strftime('%Y년 %m월 %d일 %H:%M:%S')}</p>
                    </div>
"""
        
        # 각 스크리너 타입별 브리핑 추가
        screener_labels = {
            "most_actives": "🔥 가장 거래량이 많은 종목",
            "day_gainers": "📈 당일 상승 종목",
            "day_losers": "📉 당일 하락 종목"
        }
        
        for screener_type, label in screener_labels.items():
            briefing = briefings.get(screener_type, {})
            
            if "error" in briefing:
                html += f"""
                    <div class="section">
                        <h2>{label}</h2>
                        <p class="no-data">데이터를 조회할 수 없습니다: {briefing.get('error', 'Unknown error')}</p>
                    </div>
"""
            else:
                ticker = briefing.get('ticker', 'N/A')
                top_stock = briefing.get('top_stock', {})
                price = top_stock.get('price', 0)
                change = top_stock.get('change_percent', 0)
                name = top_stock.get('name', 'Unknown')
                
                change_class = "positive" if change >= 0 else "negative"
                change_sign = "+" if change >= 0 else ""
                
                html += f"""
                    <div class="section">
                        <h2>{label}</h2>
                        <div class="stock-info">
                            <div class="ticker">{ticker} - {name}</div>
                            <div class="price">현재가: <strong>${price:.2f}</strong></div>
                            <div class="price">변동률: <strong class="{change_class}">{change_sign}{change:.2f}%</strong></div>
                            <div class="price">거래량: {top_stock.get('volume', 0):,}</div>
                        </div>
                    </div>
"""
        
        html += """
                    <div class="footer">
                        <p>This email was automatically generated by While You Were Sleeping Stock Briefing Service</p>
                        <p>© 2025 Stock Daily Briefing. All rights reserved.</p>
                    </div>
                </div>
            </body>
        </html>
"""
        return html


async def run_email_service():
    """이메일 발송 서비스 실행"""
    try:
        logger.info("=" * 50)
        logger.info("이메일 발송 서비스 시작")
        logger.info("=" * 50)
        
        service = EmailService()
        
        # 가장 최근의 브리핑 파일 찾기
        data_dir = Path(__file__).parent.parent / "output" / "data"
        report_dir = Path(__file__).parent.parent / "output" / "reports"
        
        # 가장 최신 브리핑 JSON 파일 찾기
        briefing_files = sorted(data_dir.glob("briefings_*.json"), reverse=True)
        if not briefing_files:
            logger.warning("❌ 브리핑 파일을 찾을 수 없습니다.")
            logger.info("먼저 briefing_generator.py를 실행해주세요.")
            return
        
        briefing_file = briefing_files[0]
        logger.info(f"발송할 브리핑: {briefing_file.name}")
        
        # 브리핑 데이터 로드
        with open(briefing_file, 'r', encoding='utf-8') as f:
            briefings = json.load(f)
        
        # 대응하는 마크다운 파일 찾기
        date_str = briefing_file.stem.split('_')[1]
        markdown_file = report_dir / f"briefing_{date_str}.md"
        
        if not markdown_file.exists():
            logger.warning(f"마크다운 파일을 찾을 수 없습니다: {markdown_file}")
            markdown_file = None
        
        # 이메일 발송
        success = service.send_briefing_email(briefings, markdown_file)
        
        if success:
            logger.info("\n" + "=" * 50)
            logger.info("✅ 이메일 발송 완료")
            logger.info("=" * 50)
        else:
            logger.error("\n" + "=" * 50)
            logger.error("❌ 이메일 발송 실패")
            logger.error("=" * 50)
            sys.exit(1)
        
    except Exception as e:
        logger.error(f"❌ 이메일 서비스 오류: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(run_email_service())
    except KeyboardInterrupt:
        logger.info("사용자에 의해 중단됨")
    except Exception as e:
        logger.error(f"치명적 오류: {str(e)}")
        sys.exit(1)
