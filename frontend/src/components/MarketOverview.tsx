import React, { useEffect, useState } from 'react';
import { getCompanies, getSummary } from '../api';
import { Company, SummaryData } from '../types';

interface CompanyOverview {
  company: Company;
  summary?: SummaryData;
  loading: boolean;
}

interface MarketOverviewProps {
  onSelectCompany?: (ticker: string) => void;
}

const MarketOverview: React.FC<MarketOverviewProps> = ({ onSelectCompany }) => {
  const [companies, setCompanies] = useState<CompanyOverview[]>([]);

  useEffect(() => {
    loadMarketData();
  }, []);

  const loadMarketData = async () => {
    try {
      const companiesList = await getCompanies();
      const overviewData = companiesList.map(company => ({
        company,
        loading: true
      }));
      setCompanies(overviewData);

      // Load summaries for each company
      for (const company of companiesList) {
        try {
          const summary = await getSummary(company.ticker);
          setCompanies(prev => prev.map(c => 
            c.company.ticker === company.ticker 
              ? { ...c, summary, loading: false }
              : c
          ));
        } catch (error) {
          setCompanies(prev => prev.map(c => 
            c.company.ticker === company.ticker 
              ? { ...c, loading: false }
              : c
          ));
        }
      }
    } catch (error) {
      console.error('Failed to load market data:', error);
    }
  };

  const getSentimentColor = (score?: number) => {
    if (!score) return 'bg-gray-100 text-gray-600';
    if (score > 1) return 'bg-green-100 text-green-700';
    if (score > 0) return 'bg-green-50 text-green-600';
    if (score < 0) return 'bg-red-50 text-red-600';
    return 'bg-yellow-50 text-yellow-600';
  };

  const formatPrice = (price?: string) => {
    if (!price) return 'N/A';
    return `$${price}`;
  };


  return (
    <div className="mb-8">
      <h2 className="text-2xl font-bold mb-4">Market Overview</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
        {companies.map(({ company, summary, loading }) => (
          <div 
            key={company.ticker} 
            className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow cursor-pointer p-4"
            onClick={() => onSelectCompany?.(company.ticker)}
          >
            {loading ? (
              <div className="animate-pulse">
                <div className="h-6 bg-gray-200 rounded mb-2"></div>
                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
              </div>
            ) : (
              <>
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-bold text-lg">{company.ticker}</h3>
                  <span className={`px-2 py-1 rounded text-xs font-medium ${getSentimentColor(summary?.sentiment_score)}`}>
                    {summary?.sentiment_score?.toFixed(1) || 'N/A'}
                  </span>
                </div>
                <p className="text-xs text-gray-600 mb-3 truncate">{company.name}</p>
                
                {summary?.financial_data && (
                  <div className="space-y-1">
                    <div className="flex justify-between items-baseline">
                      <span className="text-2xl font-semibold">
                        {formatPrice(summary.financial_data.currentPrice)}
                      </span>
                    </div>
                    {summary.financial_data.revenueGrowth && (
                      <div className="text-sm text-gray-600">
                        Growth: <span className="font-medium">{summary.financial_data.revenueGrowth}</span>
                      </div>
                    )}
                    {summary.financial_data.peRatio && (
                      <div className="text-sm text-gray-600">
                        P/E: <span className="font-medium">{summary.financial_data.peRatio}</span>
                      </div>
                    )}
                  </div>
                )}
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default MarketOverview;