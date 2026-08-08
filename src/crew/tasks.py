try:
    from crewai import Task, Agent
except ImportError:
    class Task:
        def __init__(self, description: str, expected_output: str, agent=None):
            self.description = description
            self.expected_output = expected_output
            self.agent = agent

    class Agent:
        pass

def create_fetch_task(agent: Agent, topic: str) -> Task:
    return Task(
        description=f"Fetch the latest trending news articles for topic: '{topic}'. Retrieve headlines, snippets, source links, and dates.",
        expected_output="JSON string or detailed list containing fetched news articles with titles, snippets, source links, and dates.",
        agent=agent
    )

def create_summarize_task(agent: Agent) -> Task:
    return Task(
        description="Process the fetched news articles. Deduplicate duplicate headlines, highlight key takeaways, and produce structured bulleted summaries.",
        expected_output="JSON string containing structured articles with headline, summary bullet points, source link, source name, and publication date.",
        agent=agent
    )

def create_distribute_task(agent: Agent) -> Task:
    return Task(
        description="Distribute the summarized news updates: post rich formatted news cards to Slack, and log the structured entries (Date, Headline, Summary, Source URL) to Google Sheets.",
        expected_output="Execution status confirmation report detailing Slack distribution and Google Sheets logging results.",
        agent=agent
    )
