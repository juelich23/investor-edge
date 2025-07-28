import React, { useState, useEffect, useCallback } from 'react';
import { Company } from '../types';
import { getCompanies } from '../api';

interface SearchBarProps {
  onSelectCompany: (ticker: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSelectCompany }) => {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [showDropdown, setShowDropdown] = useState(false);
  const [loading, setLoading] = useState(false);

  // Fetch companies based on search term
  const fetchCompanies = useCallback(async (search: string) => {
    try {
      setLoading(true);
      const data = await getCompanies(20, search || undefined);
      setCompanies(data);
    } catch (error) {
      console.error('Failed to fetch companies:', error);
      setCompanies([]);
    } finally {
      setLoading(false);
    }
  }, []);

  // Debounced search
  useEffect(() => {
    const timer = setTimeout(() => {
      fetchCompanies(searchTerm);
    }, searchTerm ? 300 : 0);

    return () => {
      clearTimeout(timer);
    };
  }, [searchTerm, fetchCompanies]);

  const filteredCompanies = companies;

  const handleSelect = (ticker: string) => {
    onSelectCompany(ticker);
    setSearchTerm('');
    setShowDropdown(false);
  };

  const formatMarketCap = (marketCap: number) => {
    if (marketCap >= 1e12) return `$${(marketCap / 1e12).toFixed(2)}T`;
    if (marketCap >= 1e9) return `$${(marketCap / 1e9).toFixed(2)}B`;
    if (marketCap >= 1e6) return `$${(marketCap / 1e6).toFixed(2)}M`;
    return `$${marketCap.toLocaleString()}`;
  };

  return (
    <div className="relative w-full max-w-md mx-auto">
      <input
        type="text"
        value={searchTerm}
        onChange={(e) => {
          setSearchTerm(e.target.value);
          setShowDropdown(true);
        }}
        onFocus={() => setShowDropdown(true)}
        placeholder="Search by ticker or company name..."
        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      
      {showDropdown && (
        <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-96 overflow-y-auto">
          {loading ? (
            <div className="px-4 py-2 text-center">
              <div className="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-gray-900"></div>
              <span className="ml-2">Searching...</span>
            </div>
          ) : filteredCompanies.length > 0 ? (
            <>
              {filteredCompanies.map(company => (
                <div
                  key={company.ticker}
                  onClick={() => handleSelect(company.ticker)}
                  className="px-4 py-3 hover:bg-gray-100 cursor-pointer border-b border-gray-100 last:border-b-0"
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="font-semibold text-lg">{company.ticker}</div>
                      <div className="text-sm text-gray-600">{company.name}</div>
                      {company.sector && (
                        <div className="text-xs text-gray-500 mt-1">{company.sector}</div>
                      )}
                    </div>
                    {company.market_cap && (
                      <div className="text-right ml-4">
                        <div className="text-xs text-gray-500">Market Cap</div>
                        <div className="text-sm font-medium">{formatMarketCap(company.market_cap)}</div>
                      </div>
                    )}
                  </div>
                </div>
              ))}
              {!searchTerm && (
                <div className="px-4 py-2 text-center text-sm text-gray-500 border-t">
                  Type to search 500+ stocks
                </div>
              )}
            </>
          ) : (
            <div className="px-4 py-2 text-gray-500">
              {searchTerm ? 'No companies found' : 'Start typing to search...'}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SearchBar;