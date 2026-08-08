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

class SummarizerInput(BaseModel):
    raw_articles_json: str = Field(description="JSON string containing raw news articles list (with title, snippet, url, source, date)")

class IntelligentSummarizerTool(BaseTool):
    name: str = "Intelligent Summarizer Tool"
    description: str = "Processes raw news articles, removes duplicate topics, highlights key points, and structures clear bulleted summaries using LLMs."
    args_schema: Type[BaseModel] = SummarizerInput

    def _run(self, raw_articles_json: str) -> str:
        try:
            articles = json.loads(raw_articles_json)
        except Exception:
            articles = [{"title": "News Article", "snippet": raw_articles_json, "url": "https://news.com"}]

        summarized_list = []
        seen_titles = set()
        
        openai_key = os.getenv("OPENAI_API_KEY")
        groq_key = os.getenv("GROQ_API_KEY")

        for art in articles:
            title = art.get("title", "").strip()
            title_key = "".join(e for e in title.lower() if e.isalnum())[:30]
            if title_key in seen_titles:
                continue
            seen_titles.add(title_key)

            snippet = art.get("snippet", "").strip()
            url = art.get("url", "#")
            source = art.get("source", "News Source")
            date = art.get("date", "Today")

            summary_text = None

            # 1. Try Groq / OpenAI LLM summarization if API key available
            if groq_key and groq_key != "your_groq_api_key_here":
                try:
                    headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
                    payload = {
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {"role": "system", "content": "You are a news summarizer assistant. Summarize the given article in 2 clear bullet points."},
                            {"role": "user", "content": f"Title: {title}\nSnippet: {snippet}"}
                        ]
                    }
                    resp = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=8)
                    if resp.status_code == 200:
                        summary_text = resp.json()["choices"][0]["message"]["content"]
                except Exception as e:
                    print(f"[SummarizerTool] Groq API error: {e}")

            elif openai_key and openai_key != "your_openai_api_key_here":
                try:
                    headers = {"Authorization": f"Bearer {openai_key}", "Content-Type": "application/json"}
                    payload = {
                        "model": "gpt-4o-mini",
                        "messages": [
                            {"role": "system", "content": "You are a news summarizer assistant. Summarize the given article in 2 clear bullet points."},
                            {"role": "user", "content": f"Title: {title}\nSnippet: {snippet}"}
                        ]
                    }
                    resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=8)
                    if resp.status_code == 200:
                        summary_text = resp.json()["choices"][0]["message"]["content"]
                except Exception as e:
                    print(f"[SummarizerTool] OpenAI API error: {e}")

            # 2. Rule-based Fallback Summary
            if not summary_text:
                summary_text = f"• **Key Highlight**: {snippet[:150]}...\n• **Impact**: Rapid technological development with market relevance."

            summarized_list.append({
                "headline": title,
                "summary": summary_text,
                "url": url,
                "source": source,
                "date": date
            })

        return json.dumps(summarized_list, indent=2, ensure_ascii=False)
