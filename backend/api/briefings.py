"""
브리핑 API 라우터
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional
import logging

from services.briefing_service import BriefingService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/briefing", tags=["Briefing"])

# 서비스 인스턴스
briefing_service = BriefingService()


class GenerateBriefingRequest(BaseModel):
    """브리핑 생성 요청"""
    ticker: str = Field(..., description="종목 코드 (예: TSLA)", min_length=1)
    type: str = Field(
        default="most_actives",
        description="스크리너 유형",
        enum=["most_actives", "day_gainers", "day_losers"]
    )


class GenerateBriefingResponse(BaseModel):
    """브리핑 생성 응답"""
    status: str = Field(..., description="상태")
    ticker: str = Field(..., description="종목 코드")
    content: str = Field(..., description="브리핑 마크다운 콘텐츠")
    message: Optional[str] = Field(None, description="메시지")


@router.post("/generate", response_model=GenerateBriefingResponse)
async def generate_briefing(request: GenerateBriefingRequest) -> GenerateBriefingResponse:
    """
    브리핑 콘텐츠 생성
    
    종목 정보와 관련 뉴스를 기반으로 마크다운 포맷의 브리핑을 생성합니다.
    
    **요청 예시**:
    ```json
    {
        "ticker": "TSLA",
        "type": "most_actives"
    }
    ```
    
    **응답 예시**:
    ```json
    {
        "status": "success",
        "ticker": "TSLA",
        "content": "# TSLA - Tesla, Inc. 브리핑\n\n...",
        "message": null
    }
    ```
    """
    try:
        # 종목 코드 대문자 변환 및 검증
        ticker = request.ticker.strip().upper()
        if not ticker:
            raise ValueError("종목 코드는 비어있을 수 없습니다.")
        
        screener_type = request.type
        # 유효한 screener_type 확인
        valid_types = {"most_actives", "day_gainers", "day_losers"}
        if screener_type not in valid_types:
            raise ValueError(f"유효하지 않은 screener_type: {screener_type}. 허용값: {list(valid_types)}")
        
        logger.info(f"브리핑 생성 시작: {ticker} (type: {screener_type})")
        
        # 브리핑 콘텐츠 생성
        briefing_content = await briefing_service.generate_briefing_content(
            ticker=ticker,
            screener_type=screener_type
        )
        
        logger.info(f"브리핑 생성 완료: {ticker}")
        
        return GenerateBriefingResponse(
            status="success",
            ticker=ticker,
            content=briefing_content,
            message=f"{ticker} 브리핑이 생성되었습니다."
        )
        
    except ValueError as e:
        logger.error(f"값 오류: {str(e)}")
        raise HTTPException(status_code=400, detail=f"요청 값 오류: {str(e)}")
    except Exception as e:
        logger.error(f"브리핑 생성 실패: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"브리핑 생성 중 오류 발생: {str(e)}"
        )


@router.get("/generate", response_model=GenerateBriefingResponse)
async def generate_briefing_get(
    ticker: str = Query(..., description="종목 코드", min_length=1),
    type: str = Query("most_actives", description="스크리너 유형")
) -> GenerateBriefingResponse:
    """
    브리핑 콘텐츠 생성 (GET 메서드)
    
    쿼리 파라미터를 사용한 브리핑 생성 (POST 메서드와 동일 기능)
    
    **쿼리 파라미터**:
    - `ticker`: 종목 코드 (필수, 예: TSLA)
    - `type`: 스크리너 유형 (선택, 기본값: most_actives, 허용값: most_actives, day_gainers, day_losers)
    """
    try:
        # 종목 코드 대문자 변환 및 검증
        ticker = ticker.strip().upper()
        if not ticker:
            raise ValueError("종목 코드는 비어있을 수 없습니다.")
        
        # 유효한 screener_type 확인
        valid_types = {"most_actives", "day_gainers", "day_losers"}
        if type not in valid_types:
            raise ValueError(f"유효하지 않은 type: {type}. 허용값: {list(valid_types)}")
        
        logger.info(f"브리핑 생성 시작 (GET): {ticker} (type: {type})")
        
        # 브리핑 콘텐츠 생성
        briefing_content = await briefing_service.generate_briefing_content(
            ticker=ticker,
            screener_type=type
        )
        
        logger.info(f"브리핑 생성 완료 (GET): {ticker}")
        
        return GenerateBriefingResponse(
            status="success",
            ticker=ticker,
            content=briefing_content,
            message=f"{ticker} 브리핑이 생성되었습니다."
        )
        
    except ValueError as e:
        logger.error(f"값 오류: {str(e)}")
        raise HTTPException(status_code=400, detail=f"요청 값 오류: {str(e)}")
    except Exception as e:
        logger.error(f"브리핑 생성 실패 (GET): {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"브리핑 생성 중 오류 발생: {str(e)}"
        )


@router.get("/")
async def list_briefings():
    """모든 브리핑 목록 조회"""
    return {
        "message": "브리핑 목록 조회",
        "briefings": []
    }


@router.get("/{briefing_id}")
async def get_briefing(briefing_id: str):
    """특정 브리핑 상세 조회"""
    return {
        "message": f"브리핑 {briefing_id} 상세 조회",
        "briefing_id": briefing_id
    }
