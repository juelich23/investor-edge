# 🧠 Investor Edge Platform - Phase 1: Earnings Intelligence MVP

**Goal:** A working dashboard that shows AI-generated earnings call summaries, sentiment scores, and KPI highlights for major public companies.

---

## ✅ Core Features to Build in Phase 1

| Feature                          | Description                                                                 |
|----------------------------------|-----------------------------------------------------------------------------|
| Earnings Transcript Scraper      | Scrape or ingest earnings calls from top 10 public companies.               |
| NLP Summary Engine (Claude/OpenAI)| Summarize calls into bullet points using LLM.                               |
| Sentiment Analyzer               | Detect tone/confidence shift (e.g., more optimistic than last Q).          |
| KPI Extractor                    | Extract structured financial metrics (Revenue, EPS, guidance).              |
| Frontend Dashboard               | Search by ticker, show summary, sentiment trend, and key metrics.           |
| Local JSON/DB Store              | Save parsed summaries and scores for display.                               |

---

## 🧩 Suggested Stack

| Component     | Tech Suggestion                    |
|---------------|------------------------------------|
| Backend       | Python + FastAPI                   |
| Scraping      | `requests` + `BeautifulSoup` or `playwright` |
| LLM API       | Claude 3, or GPT-4                 |
| Frontend      | React + Tailwind CSS               |
| Storage       | SQLite or PostgreSQL               |
| Hosting       | Local dev first, then Render/Vercel|

---

## 📅 Week-by-Week Breakdown (4 Weeks)

### ✅ Week 1: Transcript Scraper + Backend Setup
- [ ] Identify top 10 public companies (AAPL, MSFT, etc.)
- [ ] Scrape earnings transcripts from sources (Seeking Alpha, IR sites)
- [ ] Store transcripts as `.txt` or `.json`
- [ ] Setup FastAPI backend with endpoints:
  - `/api/transcripts/{ticker}`
  - `/api/summaries/{ticker}`

---

### ✅ Week 2: AI Summarization + Sentiment Engine
- [ ] Prompt Claude to summarize transcript:
  - Bullet points (performance, guidance, risks)
  - Sentiment score (-2 to +2)
- [ ] Extract KPIs: revenue, EPS, guidance
- [ ] Store results in structured JSON:
```json
{
  "ticker": "AAPL",
  "quarter": "Q2 2025",
  "summary": "...",
  "sentiment_score": 1.2,
  "kpis": {
    "revenue": "94.8B",
    "eps": "1.36",
    "guidance": "Slight growth expected in Q3"
  }
}
```

---

### ✅ Week 3: Frontend UI
- [ ] Build React app:
  - Ticker search bar
  - Card UI (summary, sentiment, KPIs)
  - Trendline of past sentiment scores (mock data OK)
- [ ] Style with Tailwind CSS
- [ ] Fetch data from API

---

### ✅ Week 4: Polish + Test
- [ ] Add loading/error states
- [ ] Cache summaries to avoid re-fetching
- [ ] “Last 5 Earnings” page (can use mock data)
- [ ] Optional: manual transcript upload

---

## 🔁 Claude Prompt Example

```
You are an earnings analyst. Read the transcript below and summarize the key points in 3 parts:
1. Overall Performance
2. Guidance or Forward Outlook
3. Risks or Concerns

Also, rate the overall sentiment of the call from -2 (very negative) to +2 (very positive) based on tone, confidence, and outlook.

Transcript: """{transcript_text}"""
```

---

## 🧪 Deliverables at End of Phase 1

- ✅ Summaries for 10 companies in local DB
- ✅ Claude-generated sentiment scores & KPIs
- ✅ Working React frontend to display results
- ✅ Ready to expand into Phase 2