try:
    from crewai import Agent
except ImportError:
    class Agent:
        def __init__(self, role: str, goal: str, backstory: str, tools: list = None, verbose: bool = True):
            self.role = role
            self.goal = goal
            self.backstory = backstory
            self.tools = tools or []
            self.verbose = verbose

from src.tools.news_fetcher_tool import NewsFetcherTool
from src.tools.summarizer_tool import IntelligentSummarizerTool
from src.tools.slack_bot_tool import SlackBotTool
from src.tools.sheets_logger_tool import SheetsLoggerTool

def create_news_fetcher_agent() -> Agent:
    return Agent(
        role="Senior News Researcher",
        goal="Discover trending news articles and fetch relevant source URLs and headlines for specified topics.",
        backstory=(
            "You are an expert news scout with a keen eye for breaking technological, financial, and AI trends. "
            "Your job is to search the web using news tools and compile fresh, relevant articles."
        ),
        tools=[NewsFetcherTool()],
        verbose=True
    )

def create_summarizer_agent() -> Agent:
    return Agent(
        role="Intelligent News Summarizer & Editor",
        goal="Distill raw news articles into concise, structured, bulleted summaries highlighting core facts.",
        backstory=(
            "You are a seasoned technology editor. You eliminate duplicate news stories, cut out fluff, "
            "and synthesize clear, actionable summaries optimized for fast reading."
        ),
        tools=[IntelligentSummarizerTool()],
        verbose=True
    )

def create_publisher_agent() -> Agent:
    return Agent(
        role="Newsroom Distribution & Archival Specialist",
        goal="Post news updates to Slack channels in real time and archive structured records into Google Sheets.",
        backstory=(
            "You manage automated communications and data pipelines. You ensure team channels are instantly updated "
            "with formatted news cards while maintaining a structured history log in Google Sheets."
        ),
        tools=[SlackBotTool(), SheetsLoggerTool()],
        verbose=True
    )
