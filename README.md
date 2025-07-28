# Investor Edge Platform - Phase 1 MVP

AI-powered earnings call analysis dashboard for major public companies.

## Features

- 📊 Earnings transcript processing for top 10 companies
- 🤖 AI-powered summarization using Claude/OpenAI
- 📈 Sentiment analysis with scoring (-2 to +2)
- 💰 KPI extraction (Revenue, EPS, Guidance)
- 🔍 Interactive search interface
- 📱 Responsive React dashboard

## Quick Start

1. **Clone and setup**
   ```bash
   cd investor
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # Copy .env.example to .env and add your API keys
   cp .env.example .env
   ```

3. **Process Earnings Data**
   ```bash
   python process_all.py
   ```

4. **Start Backend Server**
   ```bash
   uvicorn main:app --reload
   ```

5. **Frontend Setup** (new terminal)
   ```bash
   cd frontend
   npm install
   npm start
   ```

6. **Access the app**
   - Frontend: http://localhost:3000
   - API docs: http://localhost:8000/docs

## Project Structure

```
investor/
├── backend/
│   ├── main.py          # FastAPI server
│   ├── scraper.py       # Earnings transcript scraper
│   ├── ai_engine.py     # AI summarization engine
│   ├── database.py      # SQLAlchemy models
│   └── process_all.py   # Data processing script
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── api.ts       # API client
│   │   └── App.tsx      # Main app component
└── data/
    ├── transcripts/     # Raw transcript data
    └── summaries/       # AI-generated summaries
```

## API Endpoints

- `GET /api/companies` - List all available companies
- `GET /api/transcripts/{ticker}` - Get transcript for a company
- `GET /api/summaries/{ticker}` - Get AI summary for a company

## Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy
- **AI**: Claude 3 / OpenAI GPT
- **Frontend**: React, TypeScript, Tailwind CSS
- **Storage**: SQLite (upgradeable to PostgreSQL)

## Next Steps (Phase 2)

- [ ] Real-time transcript scraping
- [ ] Historical trend analysis
- [ ] Multi-quarter comparison
- [ ] Export functionality
- [ ] User authentication
- [ ] More companies coverage