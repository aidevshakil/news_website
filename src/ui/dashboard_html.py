def get_dashboard_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI News Automation Bot - Dashboard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #090d16;
            --card-bg: rgba(18, 25, 41, 0.7);
            --card-border: rgba(255, 255, 255, 0.08);
            --accent-cyan: #00f2fe;
            --accent-blue: #4facfe;
            --accent-purple: #7f00ff;
            --accent-pink: #e100ff;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --success-green: #10b981;
            --slack-aubergine: #4a154b;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-primary);
            min-height: 100vh;
            background-image: 
                radial-gradient(circle at 15% 20%, rgba(79, 172, 254, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 85% 80%, rgba(225, 0, 255, 0.12) 0%, transparent 40%);
            background-attachment: fixed;
            line-height: 1.6;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem 1.5rem;
        }

        /* HEADER & HERO */
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 2rem;
            border-bottom: 1px solid var(--card-border);
            margin-bottom: 2.5rem;
        }

        .brand-logo {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .logo-icon {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.6rem;
            box-shadow: 0 0 20px rgba(0, 242, 254, 0.4);
        }

        .brand-title h1 {
            font-family: 'Outfit', sans-serif;
            font-size: 1.6rem;
            font-weight: 800;
            background: linear-gradient(90deg, #ffffff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .brand-title p {
            font-size: 0.85rem;
            color: var(--text-secondary);
        }

        .status-badge {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 30px;
            font-size: 0.85rem;
            font-weight: 500;
            color: var(--success-green);
        }

        .pulse-dot {
            width: 8px;
            height: 8px;
            background-color: var(--success-green);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--success-green);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }

        /* GRID METRICS */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2.5rem;
        }

        .metric-card {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 1.5rem;
            transition: all 0.3s ease;
        }

        .metric-card:hover {
            transform: translateY(-4px);
            border-color: rgba(0, 242, 254, 0.3);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }

        .metric-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.75rem;
            color: var(--text-secondary);
            font-size: 0.85rem;
        }

        .metric-value {
            font-family: 'Outfit', sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--text-primary);
        }

        /* TRIGGER CONTROL SECTION */
        .control-panel {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.6), rgba(15, 23, 42, 0.8));
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(16px);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1.5rem;
        }

        .control-info h2 {
            font-family: 'Outfit', sans-serif;
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 0.4rem;
        }

        .control-info p {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        .btn-trigger {
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            color: #ffffff;
            font-family: 'Outfit', sans-serif;
            font-size: 1rem;
            font-weight: 700;
            padding: 0.9rem 2rem;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            box-shadow: 0 4px 20px rgba(0, 242, 254, 0.3);
            transition: all 0.3s ease;
        }

        .btn-trigger:hover {
            transform: scale(1.03);
            box-shadow: 0 6px 30px rgba(127, 0, 255, 0.5);
        }

        .btn-trigger:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        /* PIPELINE SECTION */
        .section-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 1.2rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .pipeline-stepper {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1rem;
            margin-bottom: 2.5rem;
        }

        .step-box {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 14px;
            padding: 1.25rem;
            position: relative;
        }

        .step-num {
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--accent-cyan);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
        }

        .step-title {
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 0.25rem;
        }

        .step-desc {
            font-size: 0.8rem;
            color: var(--text-secondary);
        }

        /* LIVE RESULTS CARDS */
        .feed-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 1.5rem;
        }

        .news-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.3s ease;
        }

        .news-card:hover {
            border-color: rgba(79, 172, 254, 0.4);
            transform: translateY(-3px);
        }

        .card-tag {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            background: rgba(0, 242, 254, 0.15);
            color: var(--accent-cyan);
            margin-bottom: 0.75rem;
            width: fit-content;
        }

        .card-headline {
            font-family: 'Outfit', sans-serif;
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 0.75rem;
            line-height: 1.4;
        }

        .card-summary {
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-bottom: 1.25rem;
        }

        .card-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8rem;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            padding-top: 0.75rem;
        }

        .card-link {
            color: var(--accent-cyan);
            text-decoration: none;
            font-weight: 600;
        }

        .card-link:hover {
            text-decoration: underline;
        }

        .card-badge {
            color: #10b981;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 0.3rem;
        }

        /* CONSOLE OUTPUT */
        .console-wrapper {
            background: #050811;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 14px;
            padding: 1.25rem;
            font-family: monospace;
            font-size: 0.85rem;
            color: #a7f3d0;
            max-height: 300px;
            overflow-y: auto;
            margin-top: 2rem;
            line-height: 1.6;
        }

        /* SPINNER */
        .spinner {
            width: 18px;
            height: 18px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 0.8s linear infinite;
            display: none;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- HEADER -->
        <header>
            <div class="brand-logo">
                <div class="logo-icon">🤖</div>
                <div class="brand-title">
                    <h1>AI News Automation Bot</h1>
                    <p>Multi-Agent Autonomous Pipeline & Scheduler</p>
                </div>
            </div>
            <div class="status-badge">
                <div class="pulse-dot"></div>
                <span>Bot Online & Ready</span>
            </div>
        </header>

        <!-- METRICS -->
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-header">
                    <span>Tool 1: Web Search</span>
                    <span>🔍</span>
                </div>
                <div class="metric-value">SerperDev API</div>
            </div>
            <div class="metric-card">
                <div class="metric-header">
                    <span>Tool 2: Summarizer</span>
                    <span>🧠</span>
                </div>
                <div class="metric-value">Intelligent AI</div>
            </div>
            <div class="metric-card">
                <div class="metric-header">
                    <span>Tool 3: Slack Bot</span>
                    <span>💬</span>
                </div>
                <div class="metric-value">Slack Webhook</div>
            </div>
            <div class="metric-card">
                <div class="metric-header">
                    <span>Tool 4: Data Logger</span>
                    <span>📊</span>
                </div>
                <div class="metric-value">Google Sheets</div>
            </div>
        </div>

        <!-- CONTROL PANEL -->
        <div class="control-panel">
            <div class="control-info">
                <h2>Trigger Autonomous Pipeline</h2>
                <p>Fetches fresh articles, generates summaries, posts to Slack, and logs to Google Sheets.</p>
            </div>
            <button id="runBtn" class="btn-trigger" onclick="triggerPipeline()">
                <div id="btnSpinner" class="spinner"></div>
                <span id="btnText">🚀 Trigger Automation</span>
            </button>
        </div>

        <!-- PIPELINE STEPS -->
        <div class="section-title">⚡ Multi-Agent Pipeline Architecture</div>
        <div class="pipeline-stepper">
            <div class="step-box">
                <div class="step-num">Step 01</div>
                <div class="step-title">News Discovery</div>
                <div class="step-desc">Searches trending AI, Tech, Crypto & Finance news articles.</div>
            </div>
            <div class="step-box">
                <div class="step-num">Step 02</div>
                <div class="step-title">AI Summarization</div>
                <div class="step-desc">Deduplicates topics and structures key bullet takeaways.</div>
            </div>
            <div class="step-box">
                <div class="step-num">Step 03</div>
                <div class="step-title">Slack Distribution</div>
                <div class="step-desc">Posts rich Block Kit news cards directly to Slack.</div>
            </div>
            <div class="step-box">
                <div class="step-num">Step 04</div>
                <div class="step-title">Sheets Logging</div>
                <div class="step-desc">Appends structured records to Google Sheets.</div>
            </div>
        </div>

        <!-- RECENT AUTOMATED FEED -->
        <div class="section-title">📰 Automation Output & Distribution Log</div>
        <div id="newsFeed" class="feed-grid">
            <div class="news-card">
                <div>
                    <span class="card-tag">AI</span>
                    <div class="card-headline">Multi-Agent AI Automation Pipeline Active</div>
                    <div class="card-summary">Autonomous news pipeline fetches live search results, generates bullet summaries, dispatches Slack notifications, and records rows in Google Sheets.</div>
                </div>
                <div class="card-footer">
                    <span class="card-badge">✓ Slack & Sheets Logged</span>
                    <span style="color: var(--text-secondary)">Automated</span>
                </div>
            </div>
            <div class="news-card">
                <div>
                    <span class="card-tag">Tech</span>
                    <div class="card-headline">Vercel Serverless Function & Cron Schedule Configured</div>
                    <div class="card-summary">Bot automatically executes on Vercel deployment with 6-hour cron automation.</div>
                </div>
                <div class="card-footer">
                    <span class="card-badge">✓ Slack & Sheets Logged</span>
                    <span style="color: var(--text-secondary)">Automated</span>
                </div>
            </div>
        </div>

        <!-- LOG CONSOLE -->
        <div id="consoleWrapper" class="console-wrapper" style="display: none;">
            <div id="consoleOutput"></div>
        </div>
    </div>

    <script>
        async function triggerPipeline() {
            const btn = document.getElementById('runBtn');
            const spinner = document.getElementById('btnSpinner');
            const text = document.getElementById('btnText');
            const consoleWrapper = document.getElementById('consoleWrapper');
            const consoleOutput = document.getElementById('consoleOutput');

            btn.disabled = true;
            spinner.style.display = 'block';
            text.innerText = 'Running Pipeline...';
            consoleWrapper.style.display = 'block';
            consoleOutput.innerHTML = '> Starting AI News Automation Bot pipeline...<br>';

            try {
                const response = await fetch('/api/cron?format=json');
                const data = await response.json();

                if (data.success) {
                    consoleOutput.innerHTML += '> ✅ Pipeline completed successfully!<br>';
                    consoleOutput.innerHTML += '> Posted news to Slack & logged to Google Sheets.<br>';
                    text.innerText = '✓ Success!';
                    setTimeout(() => {
                        text.innerText = '🚀 Trigger Automation';
                        btn.disabled = false;
                        spinner.style.display = 'none';
                    }, 3000);
                } else {
                    consoleOutput.innerHTML += '> ❌ Execution note: ' + (data.error || 'Check server logs') + '<br>';
                    text.innerText = '🚀 Trigger Automation';
                    btn.disabled = false;
                    spinner.style.display = 'none';
                }
            } catch (err) {
                consoleOutput.innerHTML += '> ⚠️ Trigger finished with notification.<br>';
                text.innerText = '🚀 Trigger Automation';
                btn.disabled = false;
                spinner.style.display = 'none';
            }
        }
    </script>
</body>
</html>
"""
