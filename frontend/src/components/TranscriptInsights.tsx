import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface TranscriptAnalysis {
  executive_summary?: string;
  raw_analysis?: string | any;
  tone_analysis?: {
    confidence_level: string;
    tone_characteristics: string[];
    tone_changes: string;
    emotional_indicators: string;
  };
  key_topics?: Array<{
    topic: string;
    description: string;
  }>;
  financial_highlights?: {
    revenue: string;
    profitability: string;
    cash_flow: string;
    guidance: string;
  };
  forward_guidance?: {
    explicit_guidance: string;
    implicit_expectations: string;
    growth_drivers: string[];
    investment_areas: string[];
    timeline: string;
  };
  management_insights?: {
    strategic_priorities: string[];
    competitive_positioning: string;
    market_opportunity: string;
    operational_focus: string[];
    capital_allocation: string;
  };
  risk_factors?: Array<{
    risk: string;
    severity: string;
    description: string;
  }>;
  qa_insights?: {
    analyst_concerns: string[];
    response_quality: string;
    deflected_topics: string[];
    new_information: string[];
  };
  notable_quotes?: string[];
  investment_implications?: {
    bull_case: string[];
    bear_case: string[];
    key_metrics: string[];
    overall_assessment: string;
  };
}

interface TranscriptInsightsProps {
  ticker: string;
  onClose?: () => void;
}

const TranscriptInsights: React.FC<TranscriptInsightsProps> = ({ ticker, onClose }) => {
  const [analysis, setAnalysis] = useState<TranscriptAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    fetchTranscriptAnalysis();
  }, [ticker]);

  const fetchTranscriptAnalysis = async () => {
    try {
      setLoading(true);
      const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await axios.get<{ analysis: TranscriptAnalysis }>(`${API_URL}/api/transcript/${ticker}`, {
        timeout: 30000 // 30 second timeout
      });
      setAnalysis(response.data.analysis);
      setError(null);
    } catch (err: any) {
      console.error('Transcript analysis error:', err);
      if (err.response) {
        setError(`Error ${err.response.status}: ${err.response.data?.detail || 'Failed to load transcript analysis'}`);
      } else if (err.code === 'ECONNABORTED') {
        setError('Request timeout - analysis is taking too long');
      } else {
        setError('Failed to load transcript analysis');
      }
    } finally {
      setLoading(false);
    }
  };

  const getConfidenceColor = (level: string) => {
    const colors: Record<string, string> = {
      'Very High': 'text-green-700 bg-green-100',
      'High': 'text-green-600 bg-green-50',
      'Moderate': 'text-yellow-600 bg-yellow-50',
      'Low': 'text-orange-600 bg-orange-50',
      'Very Low': 'text-red-600 bg-red-50'
    };
    return colors[level] || 'text-gray-600 bg-gray-50';
  };

  const getSeverityColor = (severity: string) => {
    const colors: Record<string, string> = {
      'High': 'text-red-700',
      'Medium': 'text-yellow-700',
      'Low': 'text-green-700'
    };
    return colors[severity] || 'text-gray-700';
  };

  const getAssessmentColor = (assessment: string) => {
    const colors: Record<string, string> = {
      'Highly Positive': 'text-green-700 bg-green-100',
      'Positive': 'text-green-600 bg-green-50',
      'Neutral': 'text-gray-600 bg-gray-50',
      'Negative': 'text-orange-600 bg-orange-50',
      'Highly Negative': 'text-red-600 bg-red-50'
    };
    return colors[assessment] || 'text-gray-600 bg-gray-50';
  };

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Analyzing earnings call transcript...</p>
        </div>
      </div>
    );
  }

  if (error || !analysis) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-8 max-w-md">
          <h3 className="text-lg font-semibold text-red-600 mb-2">Error</h3>
          <p className="text-gray-600">{error || 'No analysis available'}</p>
          <button
            onClick={onClose}
            className="mt-4 px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
          >
            Close
          </button>
        </div>
      </div>
    );
  }

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'tone', label: 'Tone Analysis' },
    { id: 'topics', label: 'Key Topics' },
    { id: 'guidance', label: 'Guidance Details' },
    { id: 'risks', label: 'Risk Analysis' },
    { id: 'qa', label: 'Q&A Insights' },
    { id: 'investment', label: 'Investment View' }
  ];

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-2xl max-w-6xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-600 to-blue-600 text-white p-6">
          <div className="flex justify-between items-start">
            <div>
              <h2 className="text-2xl font-bold">{ticker} Earnings Call Analysis</h2>
              <p className="text-indigo-100 mt-1">AI-Powered Transcript Insights</p>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:text-indigo-100 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        {/* Tabs */}
        <div className="border-b border-gray-200 bg-gray-50">
          <div className="flex overflow-x-auto">
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-6 py-3 text-sm font-medium whitespace-nowrap transition-colors ${
                  activeTab === tab.id
                    ? 'text-blue-600 border-b-2 border-blue-600 bg-white'
                    : 'text-gray-600 hover:text-gray-800'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto" style={{ maxHeight: 'calc(90vh - 180px)' }}>
          {activeTab === 'overview' && (
            <div className="space-y-6">
              {analysis.executive_summary === "Analysis parsing error - see raw content" && analysis.raw_analysis && (
                <div>
                  <h3 className="text-lg font-semibold mb-3 text-red-600">Analysis Parsing Error</h3>
                  <p className="text-gray-600 mb-4">The AI response couldn't be parsed properly. Raw analysis:</p>
                  <pre className="bg-gray-100 p-4 rounded-lg overflow-auto text-xs">
                    {typeof analysis.raw_analysis === 'string' 
                      ? analysis.raw_analysis.substring(0, 2000) + '...'
                      : JSON.stringify(analysis.raw_analysis, null, 2).substring(0, 2000) + '...'}
                  </pre>
                </div>
              )}
              
              {analysis.executive_summary && analysis.executive_summary !== "Analysis parsing error - see raw content" && (
                <div>
                  <h3 className="text-lg font-semibold mb-3">Executive Summary</h3>
                  <p className="text-gray-700 leading-relaxed">{analysis.executive_summary}</p>
                </div>
              )}

              {analysis.investment_implications?.overall_assessment && (
                <div>
                  <h3 className="text-lg font-semibold mb-3">Overall Assessment</h3>
                  <span className={`px-4 py-2 rounded-full font-semibold ${getAssessmentColor(analysis.investment_implications.overall_assessment)}`}>
                    {analysis.investment_implications.overall_assessment}
                  </span>
                </div>
              )}

              {analysis.financial_highlights && (
                <div>
                  <h3 className="text-lg font-semibold mb-3">Financial Highlights</h3>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <p className="text-sm text-gray-600 mb-1">Revenue</p>
                      <p className="font-semibold">{analysis.financial_highlights.revenue || 'N/A'}</p>
                    </div>
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <p className="text-sm text-gray-600 mb-1">Profitability</p>
                      <p className="font-semibold">{analysis.financial_highlights.profitability || 'N/A'}</p>
                    </div>
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <p className="text-sm text-gray-600 mb-1">Cash Flow</p>
                      <p className="font-semibold">{analysis.financial_highlights.cash_flow || 'N/A'}</p>
                    </div>
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <p className="text-sm text-gray-600 mb-1">Guidance</p>
                      <p className="font-semibold">{analysis.financial_highlights.guidance || 'N/A'}</p>
                    </div>
                  </div>
                </div>
              )}

              {analysis.notable_quotes && analysis.notable_quotes.length > 0 && (
                <div>
                  <h3 className="text-lg font-semibold mb-3">Notable Quotes</h3>
                  <div className="space-y-3">
                    {analysis.notable_quotes.map((quote, index) => (
                      <div key={index} className="border-l-4 border-blue-500 pl-4 py-2 bg-blue-50 rounded">
                        <p className="text-gray-700 italic">"{quote}"</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'tone' && analysis.tone_analysis && (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold mb-3">Management Confidence Level</h3>
                <span className={`px-4 py-2 rounded-full font-semibold ${getConfidenceColor(analysis.tone_analysis.confidence_level)}`}>
                  {analysis.tone_analysis.confidence_level}
                </span>
              </div>

              <div>
                <h3 className="text-lg font-semibold mb-3">Tone Characteristics</h3>
                <div className="flex flex-wrap gap-2">
                  {(analysis.tone_analysis.tone_characteristics || []).map((characteristic, index) => (
                    <span key={index} className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">
                      {characteristic}
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <h3 className="text-lg font-semibold mb-3">Tone Changes</h3>
                <p className="text-gray-700">{analysis.tone_analysis.tone_changes || 'N/A'}</p>
              </div>

              <div>
                <h3 className="text-lg font-semibold mb-3">Emotional Indicators</h3>
                <p className="text-gray-700">{analysis.tone_analysis.emotional_indicators || 'N/A'}</p>
              </div>
            </div>
          )}

          {activeTab === 'topics' && analysis.key_topics && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold mb-4">Key Topics Discussed</h3>
              {(analysis.key_topics || []).map((topic, index) => (
                <div key={index} className="bg-gray-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-gray-800 mb-2">{topic.topic}</h4>
                  <p className="text-gray-600">{topic.description}</p>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'guidance' && analysis.forward_guidance && (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold mb-3">Explicit Guidance</h3>
                <p className="text-gray-700">{analysis.forward_guidance.explicit_guidance || 'N/A'}</p>
              </div>

              <div>
                <h3 className="text-lg font-semibold mb-3">Implicit Expectations</h3>
                <p className="text-gray-700">{analysis.forward_guidance.implicit_expectations || 'N/A'}</p>
              </div>

              <div>
                <h3 className="text-lg font-semibold mb-3">Growth Drivers</h3>
                <ul className="list-disc list-inside space-y-1">
                  {(analysis.forward_guidance.growth_drivers || []).map((driver, index) => (
                    <li key={index} className="text-gray-700">{driver}</li>
                  ))}
                </ul>
              </div>

              <div>
                <h3 className="text-lg font-semibold mb-3">Investment Areas</h3>
                <ul className="list-disc list-inside space-y-1">
                  {(analysis.forward_guidance.investment_areas || []).map((area, index) => (
                    <li key={index} className="text-gray-700">{area}</li>
                  ))}
                </ul>
              </div>

              <div>
                <h3 className="text-lg font-semibold mb-3">Timeline</h3>
                <p className="text-gray-700">{analysis.forward_guidance.timeline || 'N/A'}</p>
              </div>
            </div>
          )}

          {activeTab === 'risks' && analysis.risk_factors && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold mb-4">Risk Factors</h3>
              {(analysis.risk_factors || []).map((risk, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="font-semibold text-gray-800">{risk.risk}</h4>
                    <span className={`text-sm font-semibold ${getSeverityColor(risk.severity)}`}>
                      {risk.severity} Risk
                    </span>
                  </div>
                  <p className="text-gray-600">{risk.description}</p>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'qa' && analysis.qa_insights && (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold mb-3">Analyst Concerns</h3>
                <ul className="list-disc list-inside space-y-1">
                  {(analysis.qa_insights.analyst_concerns || []).map((concern, index) => (
                    <li key={index} className="text-gray-700">{concern}</li>
                  ))}
                </ul>
              </div>

              <div>
                <h3 className="text-lg font-semibold mb-3">Response Quality</h3>
                <p className="text-gray-700">{analysis.qa_insights.response_quality || 'N/A'}</p>
              </div>

              {analysis.qa_insights.deflected_topics && Array.isArray(analysis.qa_insights.deflected_topics) && analysis.qa_insights.deflected_topics.length > 0 && (
                <div>
                  <h3 className="text-lg font-semibold mb-3">Deflected Topics</h3>
                  <ul className="list-disc list-inside space-y-1">
                    {analysis.qa_insights.deflected_topics.map((topic, index) => (
                      <li key={index} className="text-red-600">{topic}</li>
                    ))}
                  </ul>
                </div>
              )}

              {analysis.qa_insights.new_information && Array.isArray(analysis.qa_insights.new_information) && analysis.qa_insights.new_information.length > 0 && (
                <div>
                  <h3 className="text-lg font-semibold mb-3">New Information Revealed</h3>
                  <ul className="list-disc list-inside space-y-1">
                    {analysis.qa_insights.new_information.map((info, index) => (
                      <li key={index} className="text-green-700">{info}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {activeTab === 'investment' && analysis.investment_implications && (
            <div className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div className="bg-green-50 p-6 rounded-lg">
                  <h3 className="text-lg font-semibold mb-3 text-green-800">Bull Case</h3>
                  <ul className="space-y-2">
                    {(analysis.investment_implications.bull_case || []).map((point, index) => (
                      <li key={index} className="flex items-start">
                        <span className="text-green-600 mr-2">✓</span>
                        <span className="text-gray-700">{point}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="bg-red-50 p-6 rounded-lg">
                  <h3 className="text-lg font-semibold mb-3 text-red-800">Bear Case</h3>
                  <ul className="space-y-2">
                    {(analysis.investment_implications.bear_case || []).map((point, index) => (
                      <li key={index} className="flex items-start">
                        <span className="text-red-600 mr-2">✗</span>
                        <span className="text-gray-700">{point}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              <div>
                <h3 className="text-lg font-semibold mb-3">Key Metrics to Monitor</h3>
                <div className="flex flex-wrap gap-2">
                  {(analysis.investment_implications.key_metrics || []).map((metric, index) => (
                    <span key={index} className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
                      {metric}
                    </span>
                  ))}
                </div>
              </div>

              {analysis.management_insights && (
                <div>
                  <h3 className="text-lg font-semibold mb-3">Management Insights</h3>
                  <div className="space-y-4">
                    <div>
                      <p className="text-sm text-gray-600 mb-1">Strategic Priorities</p>
                      <ul className="list-disc list-inside space-y-1">
                        {(analysis.management_insights.strategic_priorities || []).map((priority, index) => (
                          <li key={index} className="text-gray-700">{priority}</li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600 mb-1">Competitive Positioning</p>
                      <p className="text-gray-700">{analysis.management_insights.competitive_positioning || 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600 mb-1">Market Opportunity</p>
                      <p className="text-gray-700">{analysis.management_insights.market_opportunity || 'N/A'}</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TranscriptInsights;