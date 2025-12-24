"""
StockService 단위 테스트
pytest를 사용한 주식 데이터 수집 서비스 테스트
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from services.stock_service import StockService


class TestStockServiceInit:
    """StockService 초기화 테스트"""
    
    def test_init_creates_screener(self):
        """StockService가 정상적으로 초기화되는지 테스트"""
        service = StockService()
        assert service is not None
        assert hasattr(service, 'screener')


class TestGetTrendingStocks:
    """get_trending_stocks 메서드 테스트"""
    
    @pytest.mark.asyncio
    async def test_get_trending_stocks_success_most_actives(self, mocker):
        """most_actives 스크리너 정상 동작 테스트"""
        service = StockService()
        
        # Mock 데이터 설정
        mock_screener_response = {
            'most_actives': {
                'quotes': [
                    {'symbol': 'TSLA'},
                    {'symbol': 'NVDA'},
                ]
            }
        }
        
        mock_stock_info = {
            'ticker': 'TSLA',
            'name': 'Tesla, Inc.',
            'price': 385.20,
            'change_percent': 8.7,
            'volume': 147115063,
            'market_cap': '$4,326.9B',
            'sector': 'Consumer Cyclical',
            'industry': 'Auto Manufacturers',
            'pe_ratio': '45.23',
            'status': 'success'
        }
        
        # Mock 메서드
        mocker.patch.object(service.screener, 'get_screeners', return_value=mock_screener_response)
        mocker.patch.object(service, 'get_stock_info', return_value=mock_stock_info)
        
        # 실행
        result = await service.get_trending_stocks('most_actives')
        
        # 검증
        assert result['status'] == 'success'
        assert result['screener_type'] == 'most_actives'
        assert result['top_stock']['ticker'] == 'TSLA'
        assert result['top_stock']['price'] == 385.20
        assert result['top_stock']['change_percent'] == 8.7
    
    @pytest.mark.asyncio
    async def test_get_trending_stocks_success_day_gainers(self, mocker):
        """day_gainers 스크리너 정상 동작 테스트"""
        service = StockService()
        
        mock_screener_response = {
            'day_gainers': {
                'quotes': [
                    {'symbol': 'NVDA'},
                ]
            }
        }
        
        mock_stock_info = {
            'ticker': 'NVDA',
            'name': 'NVIDIA Corporation',
            'price': 142.50,
            'change_percent': 5.2,
            'volume': 89000000,
            'market_cap': '$3,500.0B',
            'sector': 'Technology',
            'industry': 'Semiconductors',
            'pe_ratio': '52.10',
            'status': 'success'
        }
        
        mocker.patch.object(service.screener, 'get_screeners', return_value=mock_screener_response)
        mocker.patch.object(service, 'get_stock_info', return_value=mock_stock_info)
        
        result = await service.get_trending_stocks('day_gainers')
        
        assert result['status'] == 'success'
        assert result['screener_type'] == 'day_gainers'
        assert result['top_stock']['ticker'] == 'NVDA'
    
    @pytest.mark.asyncio
    async def test_get_trending_stocks_invalid_screener_type(self):
        """유효하지 않은 스크리너 타입 테스트"""
        service = StockService()
        
        result = await service.get_trending_stocks('invalid_type')
        
        assert result['status'] == 'error'
        assert result['error_type'] == 'validation_error'
        assert 'invalid_type' in result['message']
    
    @pytest.mark.asyncio
    async def test_get_trending_stocks_empty_result(self, mocker):
        """스크리너 결과가 없는 경우 테스트"""
        service = StockService()
        
        mocker.patch.object(service.screener, 'get_screeners', return_value=None)
        
        result = await service.get_trending_stocks('most_actives')
        
        assert result['status'] == 'empty'
        assert result['message'] == 'most_actives에 대한 결과가 없습니다.'
    
    @pytest.mark.asyncio
    async def test_get_trending_stocks_empty_quotes(self, mocker):
        """quotes가 비어있는 경우 테스트"""
        service = StockService()
        
        mock_screener_response = {
            'most_actives': {
                'quotes': []
            }
        }
        
        mocker.patch.object(service.screener, 'get_screeners', return_value=mock_screener_response)
        
        result = await service.get_trending_stocks('most_actives')
        
        assert result['status'] == 'empty'
    
    @pytest.mark.asyncio
    async def test_get_trending_stocks_missing_symbol(self, mocker):
        """종목 심볼이 없는 경우 테스트"""
        service = StockService()
        
        mock_screener_response = {
            'most_actives': {
                'quotes': [
                    {}  # symbol 없음
                ]
            }
        }
        
        mocker.patch.object(service.screener, 'get_screeners', return_value=mock_screener_response)
        
        result = await service.get_trending_stocks('most_actives')
        
        assert result['status'] == 'error'
        assert result['error_type'] == 'validation_error'
    
    @pytest.mark.asyncio
    async def test_get_trending_stocks_api_exception(self, mocker):
        """API 호출 중 예외 발생 테스트"""
        service = StockService()
        
        mocker.patch.object(service.screener, 'get_screeners', side_effect=Exception("API Error"))
        
        result = await service.get_trending_stocks('most_actives')
        
        assert result['status'] == 'error'
        assert result['error_type'] == 'Exception'
        assert 'API Error' in result['message']


class TestGetStockInfo:
    """get_stock_info 메서드 테스트"""
    
    @pytest.mark.asyncio
    async def test_get_stock_info_success(self, mocker):
        """종목 정보 정상 조회 테스트"""
        service = StockService()
        
        # Mock Ticker 객체
        mock_ticker = MagicMock()
        mock_ticker.asset_profile = {
            'TSLA': {
                'longName': 'Tesla, Inc.',
                'sector': 'Consumer Cyclical',
                'industry': 'Auto Manufacturers'
            }
        }
        mock_ticker.summary_detail = {
            'TSLA': {
                'regularMarketPrice': 385.20,
                'regularMarketPreviousClose': 381.50,
                'regularMarketVolume': 147115063,
                'marketCap': 4326900000000,
                'trailingPE': 45.23
            }
        }
        
        mocker.patch('services.stock_service.Ticker', return_value=mock_ticker)
        
        result = await service.get_stock_info('TSLA')
        
        assert result['status'] == 'success'
        assert result['ticker'] == 'TSLA'
        assert result['name'] == 'Tesla, Inc.'
        assert result['price'] == 385.20
        assert result['sector'] == 'Consumer Cyclical'
        assert result['industry'] == 'Auto Manufacturers'
        assert pytest.approx(result['change_percent'], 0.1) == 0.97
    
    @pytest.mark.asyncio
    async def test_get_stock_info_with_bid_ask_fallback(self, mocker):
        """bid/ask 평균 사용 테스트 (regularMarketPrice 없을 때)"""
        service = StockService()
        
        mock_ticker = MagicMock()
        mock_ticker.asset_profile = {
            'AAPL': {
                'longName': 'Apple Inc.',
                'sector': 'Technology',
                'industry': 'Consumer Electronics'
            }
        }
        mock_ticker.summary_detail = {
            'AAPL': {
                'bid': 195.50,
                'ask': 195.80,
                'regularMarketPreviousClose': 193.00,
                'regularMarketVolume': 50000000,
                'marketCap': 3000000000000,
                'trailingPE': 28.5
            }
        }
        
        mocker.patch('services.stock_service.Ticker', return_value=mock_ticker)
        
        result = await service.get_stock_info('AAPL')
        
        assert result['status'] == 'success'
        assert result['price'] == pytest.approx(195.65, 0.01)  # (195.50 + 195.80) / 2
    
    @pytest.mark.asyncio
    async def test_get_stock_info_with_open_fallback(self, mocker):
        """regularMarketOpen 사용 테스트 (regularMarketPrice, bid/ask 없을 때)"""
        service = StockService()
        
        mock_ticker = MagicMock()
        mock_ticker.asset_profile = {
            'TEST': {
                'longName': 'Test Company',
                'sector': 'Test',
                'industry': 'Test'
            }
        }
        mock_ticker.summary_detail = {
            'TEST': {
                'regularMarketOpen': 100.00,
                'regularMarketPreviousClose': 99.00,
                'regularMarketVolume': 1000000,
            }
        }
        
        mocker.patch('services.stock_service.Ticker', return_value=mock_ticker)
        
        result = await service.get_stock_info('TEST')
        
        assert result['status'] == 'success'
        assert result['price'] == 100.00
    
    @pytest.mark.asyncio
    async def test_get_stock_info_invalid_ticker_empty_string(self):
        """빈 문자열 티커 테스트"""
        service = StockService()
        
        result = await service.get_stock_info('')
        
        assert result['status'] == 'error'
    
    @pytest.mark.asyncio
    async def test_get_stock_info_invalid_ticker_none(self):
        """None 티커 테스트"""
        service = StockService()
        
        result = await service.get_stock_info(None)
        
        assert result['status'] == 'error'
    
    @pytest.mark.asyncio
    async def test_get_stock_info_ticker_uppercase_conversion(self, mocker):
        """티커 자동 대문자 변환 테스트"""
        service = StockService()
        
        mock_ticker = MagicMock()
        mock_ticker.asset_profile = {
            'TSLA': {
                'longName': 'Tesla',
                'sector': 'Consumer Cyclical',
                'industry': 'Auto'
            }
        }
        mock_ticker.summary_detail = {
            'TSLA': {
                'regularMarketPrice': 385.20,
                'regularMarketPreviousClose': 381.50,
            }
        }
        
        mocker.patch('services.stock_service.Ticker', return_value=mock_ticker)
        
        result = await service.get_stock_info('tsla')  # 소문자 입력
        
        assert result['status'] == 'success'
        assert result['ticker'] == 'TSLA'  # 대문자로 변환됨
    
    @pytest.mark.asyncio
    async def test_get_stock_info_market_cap_trillions(self, mocker):
        """시가총액 조 단위 포맷팅 테스트"""
        service = StockService()
        
        mock_ticker = MagicMock()
        mock_ticker.asset_profile = {'TSLA': {'longName': 'Tesla'}}
        mock_ticker.summary_detail = {
            'TSLA': {
                'regularMarketPrice': 100,
                'regularMarketPreviousClose': 100,
                'marketCap': 1200000000000,  # 1.2조
            }
        }
        
        mocker.patch('services.stock_service.Ticker', return_value=mock_ticker)
        
        result = await service.get_stock_info('TSLA')
        
        assert 'T' in result['market_cap']  # Trillion 표기
        assert '1.2' in result['market_cap']
    
    @pytest.mark.asyncio
    async def test_get_stock_info_market_cap_millions(self, mocker):
        """시가총액 백만 단위 포맷팅 테스트"""
        service = StockService()
        
        mock_ticker = MagicMock()
        mock_ticker.asset_profile = {'TEST': {'longName': 'Test'}}
        mock_ticker.summary_detail = {
            'TEST': {
                'regularMarketPrice': 100,
                'regularMarketPreviousClose': 100,
                'marketCap': 500000000,  # 5억
            }
        }
        
        mocker.patch('services.stock_service.Ticker', return_value=mock_ticker)
        
        result = await service.get_stock_info('TEST')
        
        assert 'M' in result['market_cap']
    
    @pytest.mark.asyncio
    async def test_get_stock_info_pe_ratio_formatting(self, mocker):
        """PER 포맷팅 테스트"""
        service = StockService()
        
        mock_ticker = MagicMock()
        mock_ticker.asset_profile = {'TSLA': {'longName': 'Tesla'}}
        mock_ticker.summary_detail = {
            'TSLA': {
                'regularMarketPrice': 100,
                'regularMarketPreviousClose': 100,
                'trailingPE': 45.2345
            }
        }
        
        mocker.patch('services.stock_service.Ticker', return_value=mock_ticker)
        
        result = await service.get_stock_info('TSLA')
        
        assert result['pe_ratio'] == '45.23'
    
    @pytest.mark.asyncio
    async def test_get_stock_info_change_percent_calculation(self, mocker):
        """변동률 계산 테스트 (0으로 나누기 방지)"""
        service = StockService()
        
        mock_ticker = MagicMock()
        mock_ticker.asset_profile = {'TEST': {'longName': 'Test'}}
        mock_ticker.summary_detail = {
            'TEST': {
                'regularMarketPrice': 110.00,
                'regularMarketPreviousClose': 100.00,
            }
        }
        
        mocker.patch('services.stock_service.Ticker', return_value=mock_ticker)
        
        result = await service.get_stock_info('TEST')
        
        assert pytest.approx(result['change_percent'], 0.01) == 10.0
    
    @pytest.mark.asyncio
    async def test_get_stock_info_zero_previous_close(self, mocker):
        """previous_close가 0인 경우 테스트"""
        service = StockService()
        
        mock_ticker = MagicMock()
        mock_ticker.asset_profile = {'TEST': {'longName': 'Test'}}
        mock_ticker.summary_detail = {
            'TEST': {
                'regularMarketPrice': 100.00,
                'regularMarketPreviousClose': 0,
            }
        }
        
        mocker.patch('services.stock_service.Ticker', return_value=mock_ticker)
        
        result = await service.get_stock_info('TEST')
        
        # 0으로 나누기 방지
        assert result['status'] == 'success'
        assert result['change_percent'] == 0
    
    @pytest.mark.asyncio
    async def test_get_stock_info_api_exception(self, mocker):
        """API 호출 중 예외 발생 테스트"""
        service = StockService()
        
        mocker.patch('services.stock_service.Ticker', side_effect=Exception("Connection Error"))
        
        result = await service.get_stock_info('TSLA')
        
        assert result['status'] == 'error'
        assert 'Connection Error' in result['error']
    
    @pytest.mark.asyncio
    async def test_get_stock_info_missing_optional_fields(self, mocker):
        """선택적 필드가 없는 경우 테스트"""
        service = StockService()
        
        mock_ticker = MagicMock()
        mock_ticker.asset_profile = {}  # 비어있음
        mock_ticker.summary_detail = {
            'TSLA': {
                'regularMarketPrice': 385.20,
            }
        }
        
        mocker.patch('services.stock_service.Ticker', return_value=mock_ticker)
        
        result = await service.get_stock_info('TSLA')
        
        assert result['status'] == 'success'
        assert result['sector'] == 'N/A'
        assert result['industry'] == 'N/A'
        assert result['market_cap'] == 'N/A'
        assert result['pe_ratio'] == 'N/A'


class TestScreenStocks:
    """screen_stocks 메서드 테스트"""
    
    @pytest.mark.asyncio
    async def test_screen_stocks_returns_empty_list(self):
        """스크리닝이 빈 리스트를 반환하는지 테스트"""
        service = StockService()
        
        criteria = {
            'minPrice': 100,
            'maxPrice': 500
        }
        
        result = await service.screen_stocks(criteria)
        
        assert isinstance(result, list)
        assert len(result) == 0
    
    @pytest.mark.asyncio
    async def test_screen_stocks_exception_handling(self, mocker):
        """스크리닝 중 예외 처리 테스트"""
        service = StockService()
        
        # screen_stocks에서 예외 발생 유도
        # (현재는 TODO이므로 직접 예외를 발생시키지 않음)
        criteria = {}
        result = await service.screen_stocks(criteria)
        
        assert isinstance(result, list)
        assert len(result) == 0


class TestIntegration:
    """통합 테스트"""
    
    @pytest.mark.asyncio
    async def test_get_trending_stocks_end_to_end(self, mocker):
        """get_trending_stocks 전체 흐름 테스트"""
        service = StockService()
        
        # 단계 1: 스크리너 결과
        mock_screener_response = {
            'most_actives': {
                'quotes': [
                    {'symbol': 'TSLA'},
                    {'symbol': 'NVDA'},
                ]
            }
        }
        
        # 단계 2: 종목 상세 정보
        mock_stock_info = {
            'ticker': 'TSLA',
            'name': 'Tesla, Inc.',
            'price': 385.20,
            'change_percent': 8.7,
            'volume': 147115063,
            'market_cap': '$4,326.9B',
            'sector': 'Consumer Cyclical',
            'industry': 'Auto Manufacturers',
            'pe_ratio': '45.23',
            'status': 'success'
        }
        
        mocker.patch.object(service.screener, 'get_screeners', return_value=mock_screener_response)
        mocker.patch.object(service, 'get_stock_info', return_value=mock_stock_info)
        
        # 실행 및 검증
        result = await service.get_trending_stocks('most_actives')
        
        assert result['status'] == 'success'
        assert result['top_stock']['ticker'] == 'TSLA'
        assert result['top_stock']['market_cap'] == '$4,326.9B'
