import React, { useState } from 'react';
import SearchBar from './components/SearchBar';
import EnhancedSummaryCard from './components/EnhancedSummaryCard';
import MarketOverview from './components/MarketOverview';
import { getSummary } from './api';
import { SummaryData } from './types';

function App() {
  const [selectedSummary, setSelectedSummary] = useState<SummaryData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSelectCompany = async (ticker: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const summary = await getSummary(ticker);
      setSelectedSummary(summary);
    } catch (err) {
      setError(`Failed to load summary for ${ticker}. Please make sure the backend is running.`);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="py-6">
            <h1 className="text-3xl font-bold text-gray-900">
              Investor Edge - Earnings Intelligence
            </h1>
            <p className="mt-2 text-gray-600">
              AI-powered earnings call analysis for major public companies
            </p>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <SearchBar onSelectCompany={handleSelectCompany} />
        </div>

        {!selectedSummary && !loading && !error && (
          <MarketOverview onSelectCompany={handleSelectCompany} />
        )}

        {loading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
            <p className="mt-2 text-gray-600">Loading earnings summary...</p>
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
            <strong className="font-bold">Error: </strong>
            <span className="block sm:inline">{error}</span>
          </div>
        )}

        {selectedSummary && !loading && !error && (
          <EnhancedSummaryCard summary={selectedSummary} />
        )}

      </main>
    </div>
  );
}

export default App;
