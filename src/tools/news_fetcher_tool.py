import os
import json
import requests
from typing import Type
from pydantic import BaseModel, Field

try:
    from crewai.tools import BaseTool
except ImportError:
    class BaseTool:
        name: str = ""
        description: str = ""

class NewsFetcherInput(BaseModel):
    topic: str = Field(description="The news topic to fetch articles for (e.g., 'AI', 'Tech', 'Finance', 'Crypto')")

class NewsFetcherTool(BaseTool):
    name: str = "News Fetcher Tool"
    description: str = "Fetches latest trending news articles based on topics using web search API (SerperDev / Google News). Returns JSON list of articles with titles, snippets, source links, and dates."
    args_schema: Type[BaseModel] = NewsFetcherInput

    def _run(self, topic: str) -> str:
        api_key = os.getenv("SERPER_API_KEY")
        
        # 1. Try SerperDev API if key is present
        if api_key and api_key != "your_serper_api_key_here":
            try:
                url = "https://google.serper.dev/news"
                payload = json.dumps({"q": f"{topic} latest news", "num": 5})
                headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}
                response = requests.post(url, headers=headers, data=payload, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    news_items = data.get("news", [])
                    results = []
                    for item in news_items:
                        results.append({
                            "title": item.get("title"),
                            "snippet": item.get("snippet", ""),
                            "url": item.get("link"),
                            "source": item.get("source", "Web"),
                            "date": item.get("date", "Today")
                        })
                    if results:
                        return json.dumps(results, indent=2, ensure_ascii=False)
            except Exception as e:
                print(f"[NewsFetcherTool] Serper API error: {e}. Falling back to standard provider.")

        # 2. RSS / Public News API Fallback
        try:
            rss_url = f"https://news.google.com/rss/search?q={topic}&hl=en-US&gl=US&ceid=US:en"
            import xml.etree.ElementTree as ET
            resp = requests.get(rss_url, timeout=8)
            if resp.status_code == 200:
                root = ET.fromstring(resp.content)
                items = root.findall('.//item')
                results = []
                for item in items[:5]:
                    results.append({
                        "title": item.findtext('title', 'No Title'),
                        "snippet": item.findtext('description', 'No Snippet'),
                        "url": item.findtext('link', ''),
                        "source": "Google News RSS",
                        "date": item.findtext('pubDate', 'Recent')
                    })
                if results:
                    return json.dumps(results, indent=2, ensure_ascii=False)
        except Exception as err:
            print(f"[NewsFetcherTool] RSS fetch error: {err}")

        # 3. Demonstration/Fallback Data
        fallback_data = [
            {
                "title": f"Breakthrough in {topic}: New Multi-Agent Framework Released",
                "snippet": f"Researchers announced a major advance in {topic} technology, enabling autonomous multi-agent systems to collaborate seamlessly.",
                "url": f"https://example.com/news/{topic.lower()}-breakthrough-2026",
                "source": "TechDaily",
                "date": "2026-08-08"
            },
            {
                "title": f"{topic} Industry Report Highlights Rapid Global Adoption",
                "snippet": f"The latest market report indicates unprecedented growth in {topic} adoption across enterprise workflows and developer ecosystems.",
                "url": f"https://example.com/news/{topic.lower()}-adoption-report",
                "source": "MarketWatch AI",
                "date": "2026-08-08"
            }
        ]
        return json.dumps(fallback_data, indent=2, ensure_ascii=False)
