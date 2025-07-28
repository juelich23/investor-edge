import axios from 'axios';
import { Company, TranscriptData, SummaryData, HistoricalData } from './types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const getCompanies = async (limit: number = 10, search?: string): Promise<Company[]> => {
  const params = new URLSearchParams();
  params.append('limit', limit.toString());
  if (search) {
    params.append('search', search);
  }
  const response = await api.get<{ companies: Company[] }>(`/api/companies?${params.toString()}`);
  return response.data.companies;
};

export const getTranscript = async (ticker: string): Promise<TranscriptData> => {
  const response = await api.get<TranscriptData>(`/api/transcripts/${ticker}`);
  return response.data;
};

export const getSummary = async (ticker: string): Promise<SummaryData> => {
  const response = await api.get<SummaryData>(`/api/summaries/${ticker}`);
  return response.data;
};

export const getHistoricalEarnings = async (ticker: string): Promise<HistoricalData> => {
  const response = await api.get<HistoricalData>(`/api/historical/${ticker}`);
  return response.data;
};