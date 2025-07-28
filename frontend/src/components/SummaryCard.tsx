import React from 'react';
import { SummaryData } from '../types';

interface SummaryCardProps {
  summary: SummaryData;
}

const SummaryCard: React.FC<SummaryCardProps> = ({ summary }) => {
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

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 max-w-4xl mx-auto">
      <div className="mb-4">
        <h2 className="text-2xl font-bold">{summary.ticker}</h2>
        <p className="text-gray-600">{summary.quarter} | {summary.date}</p>
      </div>

      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-2">Sentiment Analysis</h3>
        <div className="flex items-center space-x-4">
          <span className={`text-3xl font-bold ${getSentimentColor(summary.sentiment_score)}`}>
            {summary.sentiment_score.toFixed(1)}
          </span>
          <span className="text-lg text-gray-700">
            {getSentimentText(summary.sentiment_score)}
          </span>
        </div>
      </div>

      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-2">Key Performance Indicators</h3>
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-gray-50 p-4 rounded">
            <p className="text-sm text-gray-600">Revenue</p>
            <p className="text-xl font-semibold">{summary.kpis.revenue}</p>
          </div>
          <div className="bg-gray-50 p-4 rounded">
            <p className="text-sm text-gray-600">EPS</p>
            <p className="text-xl font-semibold">{summary.kpis.eps}</p>
          </div>
          <div className="bg-gray-50 p-4 rounded">
            <p className="text-sm text-gray-600">Guidance</p>
            <p className="text-sm font-medium">{summary.kpis.guidance}</p>
          </div>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-2">Summary</h3>
        <div className="text-gray-700 whitespace-pre-line">
          {summary.summary}
        </div>
      </div>
    </div>
  );
};

export default SummaryCard;