/**
 * FastAPI 백엔드와의 통신 함수들
 */

const API_BASE_URL = "http://localhost:8000/api";

export interface ApiStockInfo {
  status: string;
  ticker?: string;
  name?: string;
  price?: number;
  change_percent?: number;
  volume?: number;
  market_cap?: string;
  sector?: string;
  industry?: string;
  pe_ratio?: string;
  news?: ApiNewsItem[];
  error?: string;
  message?: string;
}

export interface ApiTrendingStockResponse {
  status: string;
  screener_type: "most_actives" | "day_gainers" | "day_losers";
  top_stock?: {
    ticker: string;
    name: string;
    price: number;
    change_percent: number;
    volume: number;
    market_cap?: string;
    sector?: string;
    industry?: string;
    pe_ratio?: string;
    news: ApiNewsItem[];
  };
  error?: string;
  message?: string;
}

export interface ApiNewsItem {
  title: string;
  summary: string;
  source: string;
  url: string;
  published_at: string;
  related_tickers: string[];
}

/**
 * 화제 종목 조회 API 호출
 * GET /api/stocks/trending
 */
export async function getTrendingStock(
  screenerType: "most_actives" | "day_gainers" | "day_losers" = "most_actives"
): Promise<ApiTrendingStockResponse> {
  try {
    if (!screenerType || !["most_actives", "day_gainers", "day_losers"].includes(screenerType)) {
      throw new Error(`Invalid screener type: ${screenerType}`);
    }

    const response = await fetch(
      `${API_BASE_URL}/stocks/trending?screener_type=${screenerType}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(`API Error: ${response.status} ${response.statusText} - ${error.detail || ""}`);
    }

    const data: ApiTrendingStockResponse = await response.json();
    
    // 응답 검증
    if (!data.status) {
      throw new Error("Invalid response: missing status field");
    }
    
    if (data.status === "error") {
      throw new Error(data.message || "Unknown error");
    }
    
    return data;
  } catch (error) {
    console.error("getTrendingStock error:", error);
    throw error;
  }
}

/**
 * 종목 상세 정보 조회 API 호출
 * GET /api/stocks/{ticker}
 */
export async function getStockInfo(ticker: string): Promise<ApiStockInfo> {
  try {
    // 입력 검증
    if (!ticker || typeof ticker !== "string" || ticker.trim().length === 0) {
      throw new Error("Invalid ticker: ticker must be a non-empty string");
    }

    const sanitizedTicker = ticker.toUpperCase().trim();

    const response = await fetch(`${API_BASE_URL}/stocks/${sanitizedTicker}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(`API Error: ${response.status} ${response.statusText} - ${error.detail || ""}`);
    }

    const data: ApiStockInfo = await response.json();
    
    // 응답 검증
    if (!data.status) {
      throw new Error("Invalid response: missing status field");
    }
    
    if (data.status === "error") {
      throw new Error(data.error || data.message || "Unknown error");
    }
    
    return data;
  } catch (error) {
    console.error(`getStockInfo error (${ticker}):`, error);
    throw error;
  }
}
