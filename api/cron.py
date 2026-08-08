import os
import json
from http.server import BaseHTTPRequestHandler
from src.crew.main_crew import run_news_bot

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("[Vercel Endpoint] Triggering AI News Automation Bot pipeline...")
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

    def do_POST(self):
        self.do_GET()
