import React, { useEffect, useState } from 'react';
import { SummaryData, HistoricalData } from '../types';
import { getHistoricalEarnings } from '../api';
import EarningsTrendChart from './EarningsTrendChart';
import TranscriptInsights from './TranscriptInsights';

interface EnhancedSummaryCardProps {
  summary: SummaryData;
}

const EnhancedSummaryCard: React.FC<EnhancedSummaryCardProps> = ({ summary }) => {
  const [historicalData, setHistoricalData] = useState<HistoricalData | null>(null);
  const [loadingHistorical, setLoadingHistorical] = useState(false);
  const [showTrends, setShowTrends] = useState(false);
  const [showTranscriptInsights, setShowTranscriptInsights] = useState(false);

  useEffect(() => {
    const fetchHistoricalData = async () => {
      setLoadingHistorical(true);
      try {
        const data = await getHistoricalEarnings(summary.ticker);
        setHistoricalData(data);
      } catch (error) {
        console.error('Failed to load historical data:', error);
      } finally {
        setLoadingHistorical(false);
      }
    };

    fetchHistoricalData();
  }, [summary.ticker]);
  const getSentimentColor = (score: number) => {
    if (score > 1) return 'text-green-600';
    if (score > 0) return 'text-green-500';
    if (score < -1) return 'text-red-600';
    if (score < 0) return 'text-red-500';
    return 'text-gray-600';
  };

  const getSentimentText = (score: number) => {
    if (score > 1.5) return 'Very Positive';
    if (score > 0.5) return 'Positive';
    if (score > -0.5) return 'Neutral';
    if (score > -1.5) return 'Negative';
    return 'Very Negative';
  };

  const getRecommendationColor = (rec: string) => {
    const recommendation = rec.toUpperCase();
    if (recommendation.includes('STRONG_BUY')) return 'text-green-700 bg-green-100';
    if (recommendation.includes('BUY')) return 'text-green-600 bg-green-50';
    if (recommendation.includes('HOLD')) return 'text-yellow-600 bg-yellow-50';
    if (recommendation.includes('SELL')) return 'text-red-600 bg-red-50';
    return 'text-gray-600 bg-gray-50';
  };

  const formatMarketCap = (marketCap: string) => {
    // Convert string like "3,194,468,958,208" to "3.19T"
    const num = parseFloat(marketCap.replace(/,/g, ''));
    if (num >= 1e12) return `$${(num / 1e12).toFixed(2)}T`;
    if (num >= 1e9) return `$${(num / 1e9).toFixed(2)}B`;
    if (num >= 1e6) return `$${(num / 1e6).toFixed(2)}M`;
    return `$${marketCap}`;
  };

  return (
    <div className="bg-white rounded-lg shadow-lg max-w-6xl mx-auto">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-6 rounded-t-lg">
        <div className="flex justify-between items-start">
          <div>
            <h2 className="text-3xl font-bold">{summary.ticker}</h2>
            <p className="text-blue-100 mt-1">{summary.quarter} | {summary.date}</p>
            <button
              onClick={() => setShowTranscriptInsights(true)}
              className="mt-3 px-4 py-2 bg-white bg-opacity-20 hover:bg-opacity-30 rounded-lg text-sm font-medium transition-colors flex items-center space-x-2"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <span>View Call Transcript Analysis</span>
            </button>
          </div>
          {summary.financial_data?.currentPrice && (
            <div className="text-right">
              <p className="text-3xl font-bold">${summary.financial_data.currentPrice}</p>
              <p className="text-sm text-blue-100">Current Price</p>
            </div>
          )}
        </div>
      </div>

      <div className="p-6">
        {/* Market Data Grid */}
        {summary.financial_data && (
          <div className="mb-8">
            <h3 className="text-lg font-semibold mb-4">Market Data</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {summary.financial_data.marketCap && (
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600">Market Cap</p>
                  <p className="text-lg font-semibold">{formatMarketCap(summary.financial_data.marketCap)}</p>
                </div>
              )}
              {summary.financial_data.peRatio && (
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600">P/E Ratio</p>
                  <p className="text-lg font-semibold">{summary.financial_data.peRatio}</p>
                </div>
              )}
              {summary.financial_data.yearHigh && (
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600">52W High</p>
                  <p className="text-lg font-semibold">${summary.financial_data.yearHigh}</p>
                </div>
              )}
              {summary.financial_data.yearLow && (
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600">52W Low</p>
                  <p className="text-lg font-semibold">${summary.financial_data.yearLow}</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Sentiment & Recommendation */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-6 rounded-lg">
            <h3 className="text-lg font-semibold mb-3">AI Sentiment Analysis</h3>
            <div className="flex items-center space-x-4">
              <span className={`text-4xl font-bold ${getSentimentColor(summary.sentiment_score)}`}>
                {summary.sentiment_score.toFixed(1)}
              </span>
              <div>
                <span className="text-xl font-medium text-gray-700">
                  {getSentimentText(summary.sentiment_score)}
                </span>
                <p className="text-sm text-gray-500">AI-powered analysis</p>
              </div>
            </div>
          </div>

          {summary.financial_data?.recommendation && (
            <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-6 rounded-lg">
              <h3 className="text-lg font-semibold mb-3">Analyst Consensus</h3>
              <div className="flex items-center justify-between">
                <span className={`px-4 py-2 rounded-full font-semibold ${getRecommendationColor(summary.financial_data.recommendation)}`}>
                  {summary.financial_data.recommendation}
                </span>
                {summary.financial_data.targetPrice && (
                  <div className="text-right">
                    <p className="text-sm text-gray-600">Target Price</p>
                    <p className="text-xl font-semibold">${summary.financial_data.targetPrice}</p>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Financial Performance */}
        <div className="mb-8">
          <h3 className="text-lg font-semibold mb-4">Financial Performance</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-blue-50 p-4 rounded-lg border border-blue-100">
              <p className="text-sm text-gray-600">Revenue (TTM)</p>
              <p className="text-xl font-semibold text-blue-700">{summary.kpis.revenue}</p>
            </div>
            <div className="bg-green-50 p-4 rounded-lg border border-green-100">
              <p className="text-sm text-gray-600">EPS</p>
              <p className="text-xl font-semibold text-green-700">{summary.kpis.eps}</p>
            </div>
            {summary.financial_data?.revenueGrowth && (
              <div className="bg-purple-50 p-4 rounded-lg border border-purple-100">
                <p className="text-sm text-gray-600">Revenue Growth</p>
                <p className="text-xl font-semibold text-purple-700">{summary.financial_data.revenueGrowth}</p>
              </div>
            )}
            {summary.financial_data?.profitMargins && (
              <div className="bg-orange-50 p-4 rounded-lg border border-orange-100">
                <p className="text-sm text-gray-600">Profit Margins</p>
                <p className="text-xl font-semibold text-orange-700">{summary.financial_data.profitMargins}</p>
              </div>
            )}
          </div>
        </div>

        {/* Guidance */}
        <div className="mb-8">
          <h3 className="text-lg font-semibold mb-3">Forward Guidance</h3>
          <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
            {summary.guidance ? (
              <div className="space-y-4">
                {/* Quick Summary */}
                {summary.kpis.guidance && (
                  <div>
                    <p className="font-medium text-gray-700 mb-1">Summary</p>
                    <p className="text-gray-600">{summary.kpis.guidance}</p>
                  </div>
                )}
                
                {/* Detailed Guidance Grid */}
                <div className="grid md:grid-cols-2 gap-4 mt-4">
                  {summary.guidance.revenue_guidance && summary.guidance.revenue_guidance !== 'N/A' && (
                    <div className="bg-white p-3 rounded border border-yellow-100">
                      <p className="text-sm font-medium text-gray-600">Revenue Guidance</p>
                      <p className="text-lg font-semibold text-gray-800">{summary.guidance.revenue_guidance}</p>
                    </div>
                  )}
                  {summary.guidance.eps_guidance && summary.guidance.eps_guidance !== 'N/A' && (
                    <div className="bg-white p-3 rounded border border-yellow-100">
                      <p className="text-sm font-medium text-gray-600">EPS Guidance</p>
                      <p className="text-lg font-semibold text-gray-800">{summary.guidance.eps_guidance}</p>
                    </div>
                  )}
                  {summary.guidance.growth_expectations && summary.guidance.growth_expectations !== 'N/A' && (
                    <div className="bg-white p-3 rounded border border-yellow-100">
                      <p className="text-sm font-medium text-gray-600">Growth Expectations</p>
                      <p className="text-lg font-semibold text-gray-800">{summary.guidance.growth_expectations}</p>
                    </div>
                  )}
                  {summary.guidance.guidance_confidence && summary.guidance.guidance_confidence !== 'N/A' && (
                    <div className="bg-white p-3 rounded border border-yellow-100">
                      <p className="text-sm font-medium text-gray-600">Confidence Level</p>
                      <p className={`text-lg font-semibold ${
                        summary.guidance.guidance_confidence === 'High' ? 'text-green-700' :
                        summary.guidance.guidance_confidence === 'Medium' ? 'text-yellow-700' :
                        'text-red-700'
                      }`}>
                        {summary.guidance.guidance_confidence}
                      </p>
                    </div>
                  )}
                </div>
                
                {/* Full Year Outlook */}
                {summary.guidance.full_year_guidance && summary.guidance.full_year_guidance !== 'N/A' && (
                  <div className="mt-4">
                    <p className="font-medium text-gray-700 mb-1">Full Year Outlook</p>
                    <p className="text-gray-600">{summary.guidance.full_year_guidance}</p>
                  </div>
                )}
                
                {/* Key Initiatives */}
                {summary.guidance.key_initiatives && summary.guidance.key_initiatives.length > 0 && (
                  <div className="mt-4">
                    <p className="font-medium text-gray-700 mb-2">Key Forward-Looking Initiatives</p>
                    <ul className="list-disc list-inside space-y-1">
                      {summary.guidance.key_initiatives.map((initiative, index) => (
                        <li key={index} className="text-gray-600">{initiative}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ) : (
              <p className="text-gray-700">{summary.kpis.guidance}</p>
            )}
          </div>
        </div>

        {/* AI Summary */}
        <div className="mb-8">
          <h3 className="text-lg font-semibold mb-3">AI-Generated Summary</h3>
          <div className="bg-gray-50 p-6 rounded-lg">
            <div className="text-gray-700 whitespace-pre-line space-y-2">
              {summary.summary.split('\n').map((section, index) => {
                if (section.includes('Overall Performance:')) {
                  return (
                    <div key={index}>
                      <h4 className="font-semibold text-blue-700 mb-1">📈 Overall Performance</h4>
                      <div className="pl-4">{section.replace('Overall Performance:', '')}</div>
                    </div>
                  );
                } else if (section.includes('Guidance or Forward Outlook:')) {
                  return (
                    <div key={index}>
                      <h4 className="font-semibold text-green-700 mb-1">🎯 Forward Outlook</h4>
                      <div className="pl-4">{section.replace('Guidance or Forward Outlook:', '')}</div>
                    </div>
                  );
                } else if (section.includes('Risks or Concerns:')) {
                  return (
                    <div key={index}>
                      <h4 className="font-semibold text-red-700 mb-1">⚠️ Risks & Concerns</h4>
                      <div className="pl-4">{section.replace('Risks or Concerns:', '')}</div>
                    </div>
                  );
                }
                return section ? <div key={index}>{section}</div> : null;
              })}
            </div>
          </div>
        </div>

        {/* Historical Trends Button */}
        <div className="flex justify-center">
          <button
            onClick={() => setShowTrends(!showTrends)}
            className="flex items-center space-x-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <svg className={`w-5 h-5 transform transition-transform ${showTrends ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
            <span>{showTrends ? 'Hide' : 'Show'} Historical Trends</span>
          </button>
        </div>
      </div>

      {/* Historical Trends Section */}
      {showTrends && (
        <div className="mt-0 p-6 border-t">
          {loadingHistorical ? (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <p className="mt-2 text-gray-600">Loading historical data...</p>
            </div>
          ) : historicalData ? (
            <EarningsTrendChart data={historicalData} />
          ) : (
            <div className="text-center py-12 text-gray-500">
              Unable to load historical data
            </div>
          )}
        </div>
      )}
      
      {/* Transcript Insights Modal */}
      {showTranscriptInsights && (
        <TranscriptInsights
          ticker={summary.ticker}
          onClose={() => setShowTranscriptInsights(false)}
        />
      )}
    </div>
  );
};

export default EnhancedSummaryCard;