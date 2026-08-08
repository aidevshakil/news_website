import os
import json
from http.server import BaseHTTPRequestHandler
from src.crew.main_crew import run_news_bot
from src.ui.dashboard_html import get_dashboard_html

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query_string = self.path.split('?', 1)[1] if '?' in self.path else ''
        is_json_request = ('format=json' in query_string) or (self.headers.get("x-vercel-cron") == "1") or ('application/json' in self.headers.get('Accept', ''))

        # If JSON requested or Cron triggered -> execute pipeline and return JSON
        if is_json_request:
            print("[Vercel Endpoint] Executing pipeline for JSON/Cron request...")
            try:
                results = run_news_bot(topics=["AI", "Tech", "Finance", "Crypto"])
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response_data = {
                    "status": "online",
                    "service": "AI News Automation Bot",
                    "success": True,
                    "message": "AI News Automation Bot successfully completed pipeline execution",
                    "results": results
                }
                self.wfile.write(json.dumps(response_data, indent=2).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode('utf-8'))
            return

        # Otherwise serve the beautiful Web Dashboard UI
        html_content = get_dashboard_html()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))

    def do_POST(self):
        self.do_GET()
