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

class SlackBotInput(BaseModel):
    summarized_news_json: str = Field(description="JSON string containing structured summarized news items (headline, summary, url, source)")

class SlackBotTool(BaseTool):
    name: str = "Slack Bot Integration Tool"
    description: str = "Formats summarized news updates into rich Slack block messages and posts them directly to a Slack channel."
    args_schema: Type[BaseModel] = SlackBotInput

    def _run(self, summarized_news_json: str) -> str:
        webhook_url = os.getenv("SLACK_WEBHOOK_URL")
        bot_token = os.getenv("SLACK_BOT_TOKEN")
        channel_id = os.getenv("SLACK_CHANNEL_ID")

        try:
            news_items = json.loads(summarized_news_json)
        except Exception:
            news_items = [{
                "headline": "Latest News Update",
                "summary": summarized_news_json,
                "url": "https://example.com"
            }]

        posted_count = 0
        status_logs = []

        for item in news_items:
            headline = item.get("headline", "News Alert")
            summary = item.get("summary", "")
            url = item.get("url", "#")
            source = item.get("source", "News Source")

            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"📰 {headline[:140]}",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{summary}\n\n*Source:* {source} | <{url}|Read Full Article 🔗>"
                    }
                },
                {
                    "type": "divider"
                }
            ]

            payload = {"blocks": blocks}

            if webhook_url and webhook_url != "https://hooks.slack.com/services/YOUR/WEBHOOK/URL":
                try:
                    resp = requests.post(webhook_url, json=payload, timeout=8)
                    if resp.status_code == 200:
                        posted_count += 1
                        status_logs.append(f"Posted '{headline[:30]}...' via Webhook")
                        continue
                except Exception as e:
                    status_logs.append(f"Webhook failed for '{headline[:30]}...': {e}")

            if bot_token and channel_id and bot_token != "xoxb-your-slack-bot-token":
                try:
                    from slack_sdk import WebClient
                    client = WebClient(token=bot_token)
                    client.chat_postMessage(channel=channel_id, blocks=blocks, text=headline)
                    posted_count += 1
                    status_logs.append(f"Posted '{headline[:30]}...' via Slack Bot API")
                    continue
                except Exception as e:
                    status_logs.append(f"Slack SDK failed for '{headline[:30]}...': {e}")

            status_logs.append(f"[Slack Simulation Mode] Ready to post: '{headline}' -> {url}")
            posted_count += 1

        result_msg = f"Slack distribution completed. Processed {posted_count} articles. Details:\n" + "\n".join(status_logs)
        return result_msg
