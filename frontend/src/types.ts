export interface Company {
  ticker: string;
  name: string;
  sector?: string;
  sub_industry?: string;
  exchange?: string;
  market_cap?: number;
  is_sp500?: boolean;
}

export interface TranscriptData {
  ticker: string;
  quarter: string;
  content: string;
  date: string;
}

export interface SummaryData {
  ticker: string;
  quarter: string;
  summary: string;
  sentiment_score: number;
  kpis: {
    revenue: string;
    eps: string;
    guidance: string;
  };
  date?: string;
  financial_data?: {
    currentPrice?: string;
    marketCap?: string;
    yearHigh?: string;
    yearLow?: string;
    peRatio?: string;
    revenueGrowth?: string;
    profitMargins?: string;
    epsTrailing?: string;
    recommendation?: string;
    targetPrice?: string;
  };
  guidance?: {
    revenue_guidance?: string;
    eps_guidance?: string;
    full_year_guidance?: string;
    growth_expectations?: string;
    key_initiatives?: string[];
    guidance_confidence?: string;
  };
}

export interface HistoricalQuarter {
  date: string;
  quarter: string;
  revenue: number | null;
  earnings: number | null;
  eps_actual: number | null;
  eps_estimate: number | null;
  surprise_percent: number | null;
  price_on_date: number | null;
}

export interface HistoricalMetrics {
  revenue_trend: Array<{ date: string; value: number }>;
  eps_trend: Array<{ date: string; value: number }>;
  earnings_dates: string[];
}

export interface HistoricalAnalysis {
  revenue_growth: number | null;
  eps_growth: number | null;
  avg_surprise: number | null;
  volatility: number | null;
  trend_direction: 'growing' | 'declining' | 'mixed' | 'neutral';
}

export interface HistoricalData {
  ticker: string;
  quarters: HistoricalQuarter[];
  metrics: HistoricalMetrics;
  analysis: HistoricalAnalysis;
}