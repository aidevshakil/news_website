import os
import json
from dotenv import load_dotenv

try:
    from crewai import Crew, Process
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    class Process:
        sequential = "sequential"
    class Crew:
        def __init__(self, agents, tasks, process=None, verbose=True):
            self.agents = agents
            self.tasks = tasks
            self.process = process
            self.verbose = verbose

from src.crew.agents import (
    create_news_fetcher_agent,
    create_summarizer_agent,
    create_publisher_agent
)
from src.crew.tasks import (
    create_fetch_task,
    create_summarize_task,
    create_distribute_task
)
from src.tools.news_fetcher_tool import NewsFetcherTool
from src.tools.summarizer_tool import IntelligentSummarizerTool
from src.tools.slack_bot_tool import SlackBotTool
from src.tools.sheets_logger_tool import SheetsLoggerTool

load_dotenv()

def run_news_bot(topics: list[str] = None) -> dict:
    """
    Orchestrates the Multi-Agent Crew AI Pipeline for news fetching, summarizing, 
    Slack posting, and Google Sheets logging.
    """
    if not topics:
        topics = ["AI", "Tech"]

    results_summary = {}

    for topic in topics:
        print(f"\n==================================================")
        print(f" 🚀 Executing AI News Automation Bot for Topic: {topic}")
        print(f"==================================================")

        openai_key = os.getenv("OPENAI_API_KEY")
        groq_key = os.getenv("GROQ_API_KEY")

        # If CrewAI is installed & LLM key is available, run full CrewAI orchestration
        if CREWAI_AVAILABLE and ((openai_key and openai_key != "your_openai_api_key_here") or (groq_key and groq_key != "your_groq_api_key_here")):
            try:
                fetcher_agent = create_news_fetcher_agent()
                summarizer_agent = create_summarizer_agent()
                publisher_agent = create_publisher_agent()

                fetch_task = create_fetch_task(fetcher_agent, topic)
                summarize_task = create_summarize_task(summarizer_agent)
                distribute_task = create_distribute_task(publisher_agent)

                crew = Crew(
                    agents=[fetcher_agent, summarizer_agent, publisher_agent],
                    tasks=[fetch_task, summarize_task, distribute_task],
                    process=Process.sequential,
                    verbose=True
                )

                crew_result = crew.kickoff()
                results_summary[topic] = str(crew_result)
                continue
            except Exception as e:
                print(f"[CrewAI Orchestrator] Crew execution error: {e}. Executing direct tools pipeline...")

        # Multi-Agent Tool Automation Pipeline (Executes all 4 required tools deterministically)
        fetcher_tool = NewsFetcherTool()
        summarizer_tool = IntelligentSummarizerTool()
        slack_tool = SlackBotTool()
        sheets_tool = SheetsLoggerTool()

        print(f"Step 1: Running Tool 1 (NewsFetcherTool) for {topic}...")
        raw_news_json = fetcher_tool._run(topic=topic)

        print(f"Step 2: Running Tool 2 (IntelligentSummarizerTool)...")
        summarized_json = summarizer_tool._run(raw_articles_json=raw_news_json)

        print(f"Step 3: Running Tool 3 (SlackBotTool)...")
        slack_res = slack_tool._run(summarized_news_json=summarized_json)
        print(f"Slack Status: {slack_res}")

        print(f"Step 4: Running Tool 4 (SheetsLoggerTool)...")
        sheets_res = sheets_tool._run(summarized_news_json=summarized_json)
        print(f"Sheets Status: {sheets_res}")

        results_summary[topic] = {
            "slack_status": slack_res,
            "sheets_status": sheets_res
        }

    return results_summary
