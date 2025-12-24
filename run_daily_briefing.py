#!/usr/bin/env python3
"""
Windows Task Scheduler용 로컬 자동화 스크립트
매일 정해진 시간에 실행
"""

import subprocess
import sys
from pathlib import Path
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('briefing_scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_briefing():
    """브리핑 생성 및 이메일 발송"""
    try:
        project_dir = Path(__file__).parent.parent
        backend_dir = project_dir / "backend"
        
        logger.info("=" * 60)
        logger.info("📊 일일 주식 브리핑 자동화 시작")
        logger.info("=" * 60)
        
        # 1. 화제 종목 조회
        logger.info("\n[1/3] 화제 종목 조회 중...")
        result = subprocess.run(
            [sys.executable, "-m", "services.screener_service"],
            cwd=backend_dir,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            logger.error(f"❌ 화제 종목 조회 실패:\n{result.stderr}")
            return False
        logger.info("✅ 화제 종목 조회 완료")
        
        # 2. 브리핑 생성
        logger.info("\n[2/3] 브리핑 생성 중...")
        result = subprocess.run(
            [sys.executable, "-m", "services.briefing_generator"],
            cwd=backend_dir,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            logger.error(f"❌ 브리핑 생성 실패:\n{result.stderr}")
            return False
        logger.info("✅ 브리핑 생성 완료")
        
        # 3. 이메일 발송
        logger.info("\n[3/4] 이메일 발송 중...")
        result = subprocess.run(
            [sys.executable, "-m", "services.email_service"],
            cwd=backend_dir,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            logger.warning(f"⚠️  이메일 발송 실패 (무시):\n{result.stderr}")
            logger.info("💡 로컬 .env 파일의 이메일 설정을 확인하세요.")
        else:
            logger.info("✅ 이메일 발송 완료")
        
        # 4. 인스타그램 발송
        logger.info("\n[4/5] 인스타그램 발송 중...")
        result = subprocess.run(
            [sys.executable, "-m", "services.instagram_service"],
            cwd=backend_dir,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            logger.warning(f"⚠️  인스타그램 발송 실패 (무시):\n{result.stderr}")
            logger.info("💡 .env 파일의 INSTAGRAM_USERNAME과 INSTAGRAM_PASSWORD를 설정하세요.")
        else:
            logger.info("✅ 인스타그램 발송 완료")
        
        # 5. Threads 발송
        logger.info("\n[5/5] Threads 발송 중...")
        result = subprocess.run(
            [sys.executable, "-m", "services.threads_service"],
            cwd=backend_dir,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            logger.warning(f"⚠️  Threads 발송 실패 (무시):\n{result.stderr}")
            logger.info("💡 .env 파일의 INSTAGRAM_USERNAME과 INSTAGRAM_PASSWORD를 설정하세요.")
        else:
            logger.info("✅ Threads 발송 완료")
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ 일일 주식 브리핑 자동화 완료")
        logger.info("=" * 60)
        return True
        
    except Exception as e:
        logger.error(f"❌ 오류 발생: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False


if __name__ == "__main__":
    success = run_briefing()
    sys.exit(0 if success else 1)
