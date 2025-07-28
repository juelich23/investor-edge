import os
import json
from typing import Dict, Tuple
from datetime import datetime
import anthropic
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class AIEngine:
    def __init__(self, provider="anthropic"):
        self.provider = provider
        
        if provider == "anthropic":
            self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        elif provider == "openai":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def summarize_transcript(self, transcript: str) -> Dict:
        """Generate summary, sentiment, and extract KPIs from earnings transcript"""
        
        prompt = f"""You are an experienced earnings analyst. Analyze the financial data below and provide:

1. A summary in 3 parts:
   - Overall Performance (2-3 bullet points)
   - Guidance or Forward Outlook (2-3 bullet points)
   - Risks or Concerns (2-3 bullet points)

2. Sentiment score from -2 (very negative) to +2 (very positive) based on tone, confidence, and outlook

3. Key metrics in this exact JSON format:
{{
  "revenue": "XX.XB or XX.XM",
  "eps": "X.XX",
  "guidance": "Brief guidance summary"
}}

4. Detailed forward guidance PREDICTIONS based on the financial metrics provided. Even if no explicit guidance is given, use the current metrics, growth rates, and trends to predict realistic guidance. Format as:
{{
  "revenue_guidance": "Your prediction for next quarter revenue based on current trends",
  "eps_guidance": "Your prediction for next quarter EPS based on current performance",
  "full_year_guidance": "Your prediction for full year performance",
  "growth_expectations": "Expected growth rate based on historical trends",
  "key_initiatives": ["Predicted strategic initiatives based on company sector and performance"],
  "guidance_confidence": "High/Medium/Low based on stability of metrics"
}}

Format your response as:
SUMMARY:
[Your summary here]

SENTIMENT: [score]

KPIs:
{{json metrics}}

GUIDANCE:
{{json guidance}}

IMPORTANT: For the GUIDANCE section, you MUST provide realistic predictions based on the financial data, even if no explicit guidance is mentioned. Use growth rates, margins, and sector trends to make informed predictions.

Financial Data: "{transcript}"
"""
        
        if self.provider == "anthropic":
            message = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )
            content = message.content[0].text
        else:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000
            )
            content = response.choices[0].message.content
        
        return self._parse_ai_response(content)
    
    def _parse_ai_response(self, response: str) -> Dict:
        """Parse AI response into structured format"""
        lines = response.strip().split('\n')
        
        summary = ""
        sentiment_score = 0.0
        kpis = {}
        guidance = {}
        
        current_section = None
        summary_lines = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            if line.startswith("SUMMARY:"):
                current_section = "summary"
                continue
            elif line.startswith("SENTIMENT:"):
                try:
                    sentiment_score = float(line.split(":")[-1].strip())
                except:
                    sentiment_score = 0.0
                current_section = None
                continue
            elif line.startswith("KPIs:"):
                current_section = "kpis"
                continue
            elif line.startswith("GUIDANCE:"):
                current_section = "guidance"
                continue
            
            if current_section == "summary" and line:
                summary_lines.append(line)
            elif current_section == "kpis" and line.startswith("{"):
                kpi_text = ""
                for j in range(i, len(lines)):
                    kpi_text += lines[j]
                    if "}" in lines[j]:
                        break
                try:
                    kpis = json.loads(kpi_text)
                except:
                    kpis = {
                        "revenue": "N/A",
                        "eps": "N/A",
                        "guidance": "N/A"
                    }
                current_section = None
            elif current_section == "guidance" and line.startswith("{"):
                guidance_text = ""
                for j in range(i, len(lines)):
                    guidance_text += lines[j]
                    if "}" in lines[j]:
                        break
                try:
                    guidance = json.loads(guidance_text)
                except:
                    guidance = {
                        "revenue_guidance": "N/A",
                        "eps_guidance": "N/A",
                        "full_year_guidance": "N/A",
                        "growth_expectations": "N/A",
                        "key_initiatives": [],
                        "guidance_confidence": "N/A"
                    }
                break
        
        summary = "\n".join(summary_lines)
        
        return {
            "summary": summary,
            "sentiment_score": max(-2, min(2, sentiment_score)),
            "kpis": kpis,
            "guidance": guidance
        }
    
    def analyze_sentiment_trend(self, current_score: float, previous_scores: list) -> str:
        """Analyze sentiment trend based on historical scores"""
        if not previous_scores:
            return "First analysis"
        
        avg_previous = sum(previous_scores) / len(previous_scores)
        diff = current_score - avg_previous
        
        if diff > 0.5:
            return "Significantly more positive"
        elif diff > 0.2:
            return "More positive"
        elif diff < -0.5:
            return "Significantly more negative"
        elif diff < -0.2:
            return "More negative"
        else:
            return "Stable"

class EarningsAnalyzer:
    def __init__(self):
        self.ai_engine = AIEngine()
    
    def process_transcript(self, ticker: str, transcript_data: Dict) -> Dict:
        """Process a transcript and generate summary with AI"""
        
        transcript_content = transcript_data.get("content", "")
        
        # Get AI analysis
        analysis = self.ai_engine.summarize_transcript(transcript_content)
        
        # Create summary data
        summary_data = {
            "ticker": ticker,
            "quarter": transcript_data.get("quarter", ""),
            "date": transcript_data.get("date", ""),
            "summary": analysis["summary"],
            "sentiment_score": analysis["sentiment_score"],
            "kpis": analysis["kpis"],
            "guidance": analysis.get("guidance", {}),
            "processed_at": datetime.now().isoformat()
        }
        
        return summary_data
    
    def save_summary(self, ticker: str, summary_data: Dict):
        """Save summary data to JSON file"""
        os.makedirs("../data/summaries", exist_ok=True)
        filepath = f"../data/summaries/{ticker}_latest.json"
        
        with open(filepath, 'w') as f:
            json.dump(summary_data, f, indent=2)
        
        print(f"Saved summary for {ticker} to {filepath}")

if __name__ == "__main__":
    # Test with mock transcript
    analyzer = EarningsAnalyzer()
    
    mock_transcript = {
        "ticker": "AAPL",
        "quarter": "Q1 2025",
        "date": "2025-01-25",
        "content": "Apple reported strong Q1 results with revenue of $94.8B, up 5% YoY. iPhone sales remain resilient. Services hit all-time high. EPS of $1.36 beat estimates. Management guides for slight growth in Q2. Risks include China headwinds and macro uncertainty."
    }
    
    summary = analyzer.process_transcript("AAPL", mock_transcript)
    print(json.dumps(summary, indent=2))