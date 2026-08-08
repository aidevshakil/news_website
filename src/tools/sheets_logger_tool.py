import os
import json
import csv
from datetime import datetime
from typing import Type
from pydantic import BaseModel, Field

try:
    from crewai.tools import BaseTool
except ImportError:
    class BaseTool:
        name: str = ""
        description: str = ""

class SheetsLoggerInput(BaseModel):
    summarized_news_json: str = Field(description="JSON string containing structured news items (headline, summary, url, source, date)")

class SheetsLoggerTool(BaseTool):
    name: str = "Google Sheets Logger Tool"
    description: str = "Logs structured news updates (Date, Headline, Summary, Source URL) into Google Sheets or structured record-keeping store."
    args_schema: Type[BaseModel] = SheetsLoggerInput

    def _run(self, summarized_news_json: str) -> str:
        sheet_id = os.getenv("GOOGLE_SHEET_ID")
        creds_json = os.getenv("GOOGLE_SHEETS_CREDENTIALS_JSON")

        try:
            news_items = json.loads(summarized_news_json)
        except Exception:
            news_items = [{
                "headline": "Sample Headline",
                "summary": summarized_news_json,
                "url": "https://example.com"
            }]

        today_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logged_count = 0
        logs = []

        # 1. Try Google Sheets API if credentials are available
        if sheet_id and creds_json and creds_json != '{"type": "service_account", ...}':
            try:
                import gspread
                from google.oauth2.service_account import Credentials

                # Parse JSON string (stripping optional single quotes if needed)
                if isinstance(creds_json, str):
                    creds_clean = creds_json.strip("'\"")
                    creds_dict = json.loads(creds_clean)
                else:
                    creds_dict = creds_json

                scopes = ["https://www.googleapis.com/auth/spreadsheets"]
                credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
                client = gspread.authorize(credentials)
                
                sheet = client.open_by_key(sheet_id).sheet1

                existing_records = sheet.get_all_values()
                if not existing_records:
                    sheet.append_row(["Date", "Headline", "Summary", "Source URL"])

                for item in news_items:
                    row = [
                        today_str,
                        item.get("headline", ""),
                        item.get("summary", ""),
                        item.get("url", "")
                    ]
                    sheet.append_row(row)
                    logged_count += 1
                return f"Successfully logged {logged_count} news items directly to Google Sheet (ID: {sheet_id})."
            except Exception as e:
                logs.append(f"Google Sheets API logging failed: {e}. Falling back to CSV record logger.")

        # 2. Serverless-safe CSV Fallback (writes to /tmp in serverless environments like Vercel)
        target_dir = "/tmp" if os.path.exists("/tmp") else os.getcwd()
        csv_file = os.path.join(target_dir, "news_logger_history.csv")

        try:
            file_exists = os.path.exists(csv_file)
            with open(csv_file, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["Date", "Headline", "Summary", "Source URL"])
                
                for item in news_items:
                    writer.writerow([
                        today_str,
                        item.get("headline", ""),
                        item.get("summary", ""),
                        item.get("url", "")
                    ])
                    logged_count += 1

            logs.append(f"Logged {logged_count} articles to storage file ({csv_file}).")
        except Exception as err:
            logs.append(f"Storage logging skipped: {err}")

        return "\n".join(logs)
