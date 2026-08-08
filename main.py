import sys
import os
from src.crew.main_crew import run_news_bot

if __name__ == "__main__":
    topics = sys.argv[1:] if len(sys.argv) > 1 else ["AI", "Tech", "Crypto", "Finance"]
    print("==========================================================")
    print("🤖 Starting Autonomous AI News Automation Bot")
    print(f"Target Topics: {', '.join(topics)}")
    print("==========================================================")
    
    results = run_news_bot(topics=topics)
    
    print("\n✅ Execution Finished Successfully!")
    print("Results Summary:")
    print(results)
