'use client';

import { useState, useEffect } from 'react';
import { getTrendingStock } from '@/lib/api';

interface StockInfo {
  ticker: string;
  name: string;
  price: number;
  change_percent: number;
  volume: number;
  market_cap: string;
  sector: string;
  industry: string;
  pe_ratio: string;
}

interface News {
  title: string;
  summary: string;
  url: string;
  published_at: string;
}

export default function DashboardClient() {
  const [stocks, setStocks] = useState<Record<string, any>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchAllStocks();
  }, []);

  const fetchAllStocks = async () => {
    setLoading(true);
    setError(null);

    try {
      const screeners = ['most_actives', 'day_gainers', 'day_losers'];
      
      // 타임아웃 설정 (15초)
      const fetchWithTimeout = async (screener: string) => {
        const timeoutPromise = new Promise((_, reject) =>
          setTimeout(() => reject(new Error('Request timeout')), 15000)
        );
        
        try {
          console.log(`Fetching ${screener}...`);
          const data = await Promise.race([
            getTrendingStock(screener as any),
            timeoutPromise
          ]);
          console.log(`${screener} response:`, data);
          return { screener, data };
        } catch (err) {
          console.error(`Failed to fetch ${screener}:`, err);
          return {
            screener,
            data: {
              status: 'error',
              message: `${screener} 데이터를 가져올 수 없습니다.`
            }
          };
        }
      };

      // 병렬로 모든 요청 실행
      const results = await Promise.all(
        screeners.map(screener => fetchWithTimeout(screener))
      );

      const stocksData: Record<string, any> = {};
      results.forEach(({ screener, data }) => {
        stocksData[screener] = data;
      });

      setStocks(stocksData);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Unknown error';
      setError(`Failed to load stocks: ${errorMsg}`);
      console.error('Stock fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  const renderStockCard = (screenerType: string, data: any) => {
    if (!data || data.status !== 'success' || !data.top_stock) {
      return (
        <div className="bg-white rounded-lg shadow p-6 h-full">
          <h3 className="text-lg font-semibold mb-4 capitalize">
            {screenerType.replace('_', ' ')}
          </h3>
          <p className="text-gray-500">데이터를 불러올 수 없습니다.</p>
        </div>
      );
    }

    const stock = data.top_stock as StockInfo;
    const isPositive = stock.change_percent >= 0;
    const changeColor = isPositive ? 'text-green-600' : 'text-red-600';

    return (
      <div className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6 h-full">
        <h3 className="text-lg font-semibold mb-4 capitalize">
          {screenerType.replace('_', ' ')}
        </h3>

        <div className="space-y-3">
          {/* 종목명 */}
          <div>
            <p className="text-sm text-gray-600">종목</p>
            <p className="text-2xl font-bold text-blue-600">{stock.ticker}</p>
            <p className="text-sm text-gray-600">{stock.name}</p>
          </div>

          {/* 가격 및 변동률 */}
          <div className="grid grid-cols-2 gap-4 pt-2 border-t">
            <div>
              <p className="text-xs text-gray-600">현재가</p>
              <p className="text-xl font-bold">${stock.price.toFixed(2)}</p>
            </div>
            <div>
              <p className="text-xs text-gray-600">변동률</p>
              <p className={`text-xl font-bold ${changeColor}`}>
                {isPositive ? '+' : ''}{stock.change_percent.toFixed(2)}%
              </p>
            </div>
          </div>

          {/* 거래량 */}
          <div className="pt-2 border-t">
            <p className="text-xs text-gray-600">거래량</p>
            <p className="text-sm font-medium">
              {stock.volume.toLocaleString()}
            </p>
          </div>

          {/* 시가총액 */}
          <div>
            <p className="text-xs text-gray-600">시가총액</p>
            <p className="text-sm font-medium">{stock.market_cap}</p>
          </div>

          {/* 섹터/산업 */}
          <div className="grid grid-cols-2 gap-2 pt-2 border-t">
            <div>
              <p className="text-xs text-gray-600">섹터</p>
              <p className="text-xs font-medium">{stock.sector}</p>
            </div>
            <div>
              <p className="text-xs text-gray-600">산업</p>
              <p className="text-xs font-medium">{stock.industry}</p>
            </div>
          </div>

          {/* PER */}
          <div>
            <p className="text-xs text-gray-600">PER</p>
            <p className="text-sm font-medium">{stock.pe_ratio}</p>
          </div>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-4xl font-bold mb-8">
            당신이 잠든 사이 📈
          </h1>
          <div className="text-center py-20">
            <p className="text-gray-600">로딩 중...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        {/* 헤더 */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">
            당신이 잠든 사이 📈
          </h1>
          <p className="text-gray-600">
            {new Date().toLocaleDateString('ko-KR', {
              year: 'numeric',
              month: 'long',
              day: 'numeric',
            })}
          </p>
        </div>

        {/* 에러 메시지 */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {/* 종목 카드 그리드 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {renderStockCard(
            'most_actives',
            stocks['most_actives']
          )}
          {renderStockCard(
            'day_gainers',
            stocks['day_gainers']
          )}
          {renderStockCard(
            'day_losers',
            stocks['day_losers']
          )}
        </div>

        {/* 새로고침 버튼 */}
        <div className="mt-8 text-center">
          <button
            onClick={fetchAllStocks}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold py-2 px-6 rounded-lg transition-colors"
          >
            {loading ? '새로고침 중...' : '새로고침'}
          </button>
        </div>
      </div>
    </div>
  );
}


