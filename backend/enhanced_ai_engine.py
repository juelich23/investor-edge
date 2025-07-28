import os
import json
from typing import Dict, List, Tuple
from datetime import datetime
import anthropic
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class EnhancedAIEngine:
    def __init__(self, provider="anthropic"):
        self.provider = provider
        
        if provider == "anthropic":
            self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        elif provider == "openai":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def analyze_earnings_call(self, transcript: str, financial_data: str) -> Dict:
        """
        Comprehensive analysis of earnings call transcript including tone, topics, and insights
        """
        
        prompt = f"""You are an expert financial analyst specializing in earnings call analysis. 
        Analyze the following earnings call transcript along with the financial data and provide:

1. EXECUTIVE SUMMARY (3-4 sentences)
   Provide a concise overview of the key takeaways from the earnings call.

2. TONE ANALYSIS
   Analyze the overall tone and sentiment of management during the call:
   - Management confidence level (Very High/High/Moderate/Low/Very Low)
   - Tone characteristics (e.g., optimistic, cautious, defensive, transparent)
   - Notable changes in tone when discussing different topics
   - Key emotional indicators and their implications

3. KEY TOPICS DISCUSSED
   List the 5-7 most important topics covered in the call with brief descriptions.

4. FINANCIAL HIGHLIGHTS
   Extract and summarize the key financial metrics mentioned:
   - Revenue figures and growth rates
   - Profitability metrics
   - Cash flow and balance sheet items
   - Any financial guidance provided

5. FORWARD GUIDANCE ANALYSIS
   Based on the transcript, provide detailed forward-looking insights:
   - Explicit guidance provided by management
   - Implicit expectations based on management commentary
   - Growth drivers mentioned
   - Investment areas highlighted
   - Timeline for key initiatives

6. MANAGEMENT INSIGHTS
   Analyze management's commentary for deeper insights:
   - Strategic priorities
   - Competitive positioning
   - Market opportunity assessment
   - Operational focus areas
   - Capital allocation strategy

7. RISK FACTORS
   Identify and assess risks mentioned or implied:
   - Explicitly stated risks
   - Implied concerns based on defensive responses
   - Macro environment impacts
   - Competitive threats
   - Execution risks

8. ANALYST Q&A INSIGHTS
   If Q&A section is present, analyze:
   - Key analyst concerns
   - Quality of management responses
   - Any deflection or avoidance of topics
   - Surprises or new information revealed

9. NOTABLE QUOTES
   Extract 3-5 most impactful direct quotes from management.

10. INVESTMENT IMPLICATIONS
    Based on the analysis, provide:
    - Bull case factors
    - Bear case factors
    - Key metrics to monitor
    - Overall assessment (Highly Positive/Positive/Neutral/Negative/Highly Negative)

Format your response as ONLY valid JSON (no text before or after) with these exact keys:
{{
  "executive_summary": "...",
  "tone_analysis": {{
    "confidence_level": "...",
    "tone_characteristics": ["..."],
    "tone_changes": "...",
    "emotional_indicators": "..."
  }},
  "key_topics": [
    {{"topic": "...", "description": "..."}}
  ],
  "financial_highlights": {{
    "revenue": "...",
    "profitability": "...",
    "cash_flow": "...",
    "guidance": "..."
  }},
  "forward_guidance": {{
    "explicit_guidance": "...",
    "implicit_expectations": "...",
    "growth_drivers": ["..."],
    "investment_areas": ["..."],
    "timeline": "..."
  }},
  "management_insights": {{
    "strategic_priorities": ["..."],
    "competitive_positioning": "...",
    "market_opportunity": "...",
    "operational_focus": ["..."],
    "capital_allocation": "..."
  }},
  "risk_factors": [
    {{"risk": "...", "severity": "High/Medium/Low", "description": "..."}}
  ],
  "qa_insights": {{
    "analyst_concerns": ["..."],
    "response_quality": "...",
    "deflected_topics": ["..."],
    "new_information": ["..."]
  }},
  "notable_quotes": ["..."],
  "investment_implications": {{
    "bull_case": ["..."],
    "bear_case": ["..."],
    "key_metrics": ["..."],
    "overall_assessment": "..."
  }}
}}

EARNINGS CALL TRANSCRIPT:
{transcript}

FINANCIAL DATA:
{financial_data}
"""
        
        if self.provider == "anthropic":
            # Add JSON instruction
            json_prompt = prompt + "\n\nIMPORTANT: Return ONLY valid JSON, starting with { and ending with }. No other text."
            
            message = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=4000,
                temperature=0.3,
                messages=[{"role": "user", "content": json_prompt}]
            )
            content = message.content[0].text
        else:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-16k",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=4000
            )
            content = response.choices[0].message.content
        
        try:
            # Parse JSON response
            analysis = json.loads(content)
            return analysis
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Raw response (first 1000 chars): {content[:1000]}")
            
            # Try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                try:
                    analysis = json.loads(json_match.group())
                    print("Successfully extracted JSON from response")
                    return analysis
                except:
                    pass
            
            # Fallback parsing if JSON is malformed
            return self._parse_text_response(content)
    
    def _parse_text_response(self, response: str) -> Dict:
        """Fallback parser for non-JSON responses"""
        # Basic parsing logic for fallback
        return {
            "executive_summary": "Analysis parsing error - see raw content",
            "raw_analysis": response,
            "tone_analysis": {
                "confidence_level": "Unknown",
                "tone_characteristics": [],
                "tone_changes": "Unable to parse",
                "emotional_indicators": "Unable to parse"
            },
            "investment_implications": {
                "overall_assessment": "Neutral"
            }
        }
    
    def compare_to_previous_calls(self, current_analysis: Dict, previous_analyses: List[Dict]) -> Dict:
        """Compare current call to previous calls to identify trends"""
        if not previous_analyses:
            return {
                "tone_trend": "No historical data",
                "topic_evolution": "No historical data",
                "guidance_consistency": "No historical data"
            }
        
        # Analyze trends
        tone_trend = self._analyze_tone_trend(current_analysis, previous_analyses)
        topic_evolution = self._analyze_topic_evolution(current_analysis, previous_analyses)
        guidance_consistency = self._analyze_guidance_consistency(current_analysis, previous_analyses)
        
        return {
            "tone_trend": tone_trend,
            "topic_evolution": topic_evolution,
            "guidance_consistency": guidance_consistency,
            "momentum": self._calculate_momentum(current_analysis, previous_analyses)
        }
    
    def _analyze_tone_trend(self, current: Dict, previous: List[Dict]) -> str:
        """Analyze how management tone has changed over time"""
        # Implementation for tone trend analysis
        confidence_levels = {
            "Very High": 5, "High": 4, "Moderate": 3, "Low": 2, "Very Low": 1
        }
        
        current_confidence = confidence_levels.get(
            current.get("tone_analysis", {}).get("confidence_level", "Moderate"), 3
        )
        
        if previous:
            prev_confidence = confidence_levels.get(
                previous[-1].get("tone_analysis", {}).get("confidence_level", "Moderate"), 3
            )
            
            if current_confidence > prev_confidence:
                return "Improving - Management confidence increasing"
            elif current_confidence < prev_confidence:
                return "Deteriorating - Management confidence decreasing"
            else:
                return "Stable - Management confidence unchanged"
        
        return "Baseline established"
    
    def _analyze_topic_evolution(self, current: Dict, previous: List[Dict]) -> str:
        """Analyze how key topics have evolved"""
        # Extract current topics
        current_topics = [t["topic"] for t in current.get("key_topics", [])]
        
        if previous and previous[-1].get("key_topics"):
            prev_topics = [t["topic"] for t in previous[-1].get("key_topics", [])]
            
            new_topics = set(current_topics) - set(prev_topics)
            dropped_topics = set(prev_topics) - set(current_topics)
            
            evolution = []
            if new_topics:
                evolution.append(f"New focus areas: {', '.join(new_topics)}")
            if dropped_topics:
                evolution.append(f"De-emphasized: {', '.join(dropped_topics)}")
            
            return " | ".join(evolution) if evolution else "Consistent focus areas"
        
        return "Initial topic baseline"
    
    def _analyze_guidance_consistency(self, current: Dict, previous: List[Dict]) -> str:
        """Analyze consistency of guidance over time"""
        # This would compare guidance metrics over time
        return "Guidance tracking initialized"
    
    def _calculate_momentum(self, current: Dict, previous: List[Dict]) -> str:
        """Calculate overall momentum based on multiple factors"""
        assessment_scores = {
            "Highly Positive": 5, "Positive": 4, "Neutral": 3, 
            "Negative": 2, "Highly Negative": 1
        }
        
        current_score = assessment_scores.get(
            current.get("investment_implications", {}).get("overall_assessment", "Neutral"), 3
        )
        
        if previous:
            recent_scores = [
                assessment_scores.get(
                    p.get("investment_implications", {}).get("overall_assessment", "Neutral"), 3
                ) for p in previous[-3:]  # Last 3 quarters
            ]
            
            avg_recent = sum(recent_scores) / len(recent_scores)
            
            if current_score > avg_recent + 0.5:
                return "Accelerating positive momentum"
            elif current_score < avg_recent - 0.5:
                return "Deteriorating momentum"
            else:
                return "Stable momentum"
        
        return "Momentum baseline established"

class TranscriptProcessor:
    def __init__(self):
        self.ai_engine = EnhancedAIEngine()
    
    def process_full_transcript(self, ticker: str, transcript_data: Dict, financial_data: Dict) -> Dict:
        """Process a full earnings call transcript"""
        
        # Prepare financial data summary for context
        financial_context = self._prepare_financial_context(financial_data)
        
        # Analyze the transcript
        analysis = self.ai_engine.analyze_earnings_call(
            transcript_data.get("content", ""),
            financial_context
        )
        
        # Load historical analyses if available
        historical = self._load_historical_analyses(ticker)
        
        # Compare to previous calls
        trends = self.ai_engine.compare_to_previous_calls(analysis, historical)
        
        # Combine everything
        complete_analysis = {
            "ticker": ticker,
            "date": transcript_data.get("date", datetime.now().strftime("%Y-%m-%d")),
            "quarter": transcript_data.get("quarter", ""),
            "source": transcript_data.get("source", ""),
            "analysis": analysis,
            "trends": trends,
            "has_full_transcript": True,
            "transcript_length": len(transcript_data.get("content", "")),
            "processed_at": datetime.now().isoformat()
        }
        
        # Save the analysis
        self._save_analysis(ticker, complete_analysis)
        
        return complete_analysis
    
    def _prepare_financial_context(self, financial_data: Dict) -> str:
        """Prepare financial data as context for AI analysis"""
        context_parts = []
        
        if financial_data:
            context_parts.append(f"Current Price: ${financial_data.get('currentPrice', 'N/A')}")
            context_parts.append(f"Market Cap: ${financial_data.get('marketCap', 'N/A')}")
            context_parts.append(f"P/E Ratio: {financial_data.get('peRatio', 'N/A')}")
            context_parts.append(f"Revenue Growth: {financial_data.get('revenueGrowth', 'N/A')}")
            context_parts.append(f"Profit Margins: {financial_data.get('profitMargins', 'N/A')}")
            context_parts.append(f"Analyst Rating: {financial_data.get('recommendation', 'N/A')}")
        
        return "\n".join(context_parts)
    
    def _load_historical_analyses(self, ticker: str) -> List[Dict]:
        """Load previous transcript analyses for comparison"""
        historical = []
        
        # Look for previous analyses
        analysis_dir = f"../data/analyses/{ticker}"
        if os.path.exists(analysis_dir):
            files = sorted([f for f in os.listdir(analysis_dir) if f.endswith('.json')])
            
            # Load last 4 quarters
            for file in files[-4:]:
                with open(os.path.join(analysis_dir, file), 'r') as f:
                    historical.append(json.load(f))
        
        return historical
    
    def _save_analysis(self, ticker: str, analysis: Dict):
        """Save transcript analysis"""
        # Create directory structure
        analysis_dir = f"../data/analyses/{ticker}"
        os.makedirs(analysis_dir, exist_ok=True)
        
        # Save with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(analysis_dir, f"{ticker}_analysis_{timestamp}.json")
        
        with open(filepath, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        # Also save as latest
        latest_path = os.path.join("../data/analyses", f"{ticker}_latest_analysis.json")
        with open(latest_path, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        print(f"✓ Saved transcript analysis to {filepath}")

if __name__ == "__main__":
    # Test the enhanced AI engine
    processor = TranscriptProcessor()
    
    # Mock test data
    test_transcript = {
        "content": "CEO: We delivered strong results this quarter with revenue up 25% year-over-year...",
        "date": "2024-01-25",
        "quarter": "Q4 2023"
    }
    
    test_financial = {
        "currentPrice": "150.00",
        "marketCap": "100000000000",
        "peRatio": "25.5",
        "revenueGrowth": "0.25"
    }
    
    result = processor.process_full_transcript("TEST", test_transcript, test_financial)
    print(json.dumps(result, indent=2))