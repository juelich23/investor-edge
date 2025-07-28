import React from 'react';
import {
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ComposedChart,
  Cell
} from 'recharts';
import { HistoricalData } from '../types';

interface EarningsTrendChartProps {
  data: HistoricalData;
}

const EarningsTrendChart: React.FC<EarningsTrendChartProps> = ({ data }) => {
  // Prepare data for revenue and EPS chart
  const quarterlyData = data.quarters.slice(0, 8).reverse().map(q => ({
    quarter: q.quarter,
    revenue: q.revenue, // Already in millions from the data source
    eps: q.eps_actual,
    surprise: q.surprise_percent
  }));

  // Format currency values
  const formatCurrency = (value: number) => {
    if (value >= 1000) {
      return `$${(value / 1000).toFixed(1)}B`;
    }
    return `$${value.toFixed(0)}M`;
  };

  // Format percentage
  const formatPercent = (value: number) => `${value?.toFixed(1)}%`;

  // Get trend indicator color
  const getTrendColor = (value: number | null) => {
    if (!value) return 'text-gray-500';
    return value > 0 ? 'text-green-600' : 'text-red-600';
  };

  // Get trend arrow
  const getTrendArrow = (value: number | null) => {
    if (!value) return '→';
    return value > 0 ? '↑' : '↓';
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6">Historical Earnings Trends</h2>
      
      {/* Key Metrics Summary */}
      <div className="grid grid-cols-4 gap-4 mb-8">
        <div className="bg-gray-50 p-4 rounded-lg">
          <p className="text-sm text-gray-600">Revenue Growth (YoY)</p>
          <p className={`text-2xl font-bold ${getTrendColor(data.analysis.revenue_growth)}`}>
            {data.analysis.revenue_growth ? formatPercent(data.analysis.revenue_growth) : 'N/A'} 
            <span className="ml-1">{getTrendArrow(data.analysis.revenue_growth)}</span>
          </p>
        </div>
        <div className="bg-gray-50 p-4 rounded-lg">
          <p className="text-sm text-gray-600">EPS Growth (YoY)</p>
          <p className={`text-2xl font-bold ${getTrendColor(data.analysis.eps_growth)}`}>
            {data.analysis.eps_growth ? formatPercent(data.analysis.eps_growth) : 'N/A'}
            <span className="ml-1">{getTrendArrow(data.analysis.eps_growth)}</span>
          </p>
        </div>
        <div className="bg-gray-50 p-4 rounded-lg">
          <p className="text-sm text-gray-600">Avg Earnings Surprise</p>
          <p className={`text-2xl font-bold ${getTrendColor(data.analysis.avg_surprise)}`}>
            {data.analysis.avg_surprise ? formatPercent(data.analysis.avg_surprise) : 'N/A'}
          </p>
        </div>
        <div className="bg-gray-50 p-4 rounded-lg">
          <p className="text-sm text-gray-600">Trend Direction</p>
          <p className="text-2xl font-bold capitalize">
            {data.analysis.trend_direction}
          </p>
        </div>
      </div>

      {/* Revenue and EPS Trend Chart */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold mb-4">Revenue & EPS Trends</h3>
        <ResponsiveContainer width="100%" height={400}>
          <ComposedChart data={quarterlyData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="quarter" />
            <YAxis yAxisId="left" tickFormatter={formatCurrency} />
            <YAxis yAxisId="right" orientation="right" />
            <Tooltip 
              formatter={(value: any, name: string) => {
                if (name === 'Revenue') return formatCurrency(value);
                if (name === 'EPS') return `$${value?.toFixed(2)}`;
                return value;
              }}
            />
            <Legend />
            <Bar yAxisId="left" dataKey="revenue" fill="#3B82F6" name="Revenue" />
            <Line yAxisId="right" type="monotone" dataKey="eps" stroke="#10B981" strokeWidth={3} name="EPS" dot={{ fill: '#10B981' }} />
          </ComposedChart>
        </ResponsiveContainer>
      </div>

      {/* Earnings Surprise Chart */}
      <div>
        <h3 className="text-lg font-semibold mb-4">Earnings Surprise %</h3>
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={quarterlyData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="quarter" />
            <YAxis tickFormatter={formatPercent} />
            <Tooltip formatter={(value: any) => formatPercent(value)} />
            <Bar 
              dataKey="surprise" 
              name="Surprise %" 
              fill="#3B82F6"
            >
              {quarterlyData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.surprise && entry.surprise > 0 ? '#10B981' : '#EF4444'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Recent Quarters Table */}
      <div className="mt-8">
        <h3 className="text-lg font-semibold mb-4">Recent Quarter Details</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quarter</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Revenue</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">EPS Actual</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">EPS Est.</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Surprise</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Stock Price</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {data.quarters.slice(0, 4).map((quarter, index) => (
                <tr key={index}>
                  <td className="px-4 py-2 whitespace-nowrap text-sm font-medium text-gray-900">{quarter.quarter}</td>
                  <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-900">
                    {quarter.revenue ? formatCurrency(quarter.revenue) : 'N/A'}
                  </td>
                  <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-900">
                    ${quarter.eps_actual?.toFixed(2) || 'N/A'}
                  </td>
                  <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-900">
                    ${quarter.eps_estimate?.toFixed(2) || 'N/A'}
                  </td>
                  <td className={`px-4 py-2 whitespace-nowrap text-sm font-medium ${quarter.surprise_percent && quarter.surprise_percent > 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {quarter.surprise_percent ? formatPercent(quarter.surprise_percent) : 'N/A'}
                  </td>
                  <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-900">
                    ${quarter.price_on_date?.toFixed(2) || 'N/A'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default EarningsTrendChart;