# -*- coding: utf-8 -*-
"""
BanglaMultiScript Interactive Web UI
Provides a web interface to convert sentences live with real-time preview and copy buttons.
Runs with zero external dependencies using Python standard library (http.server) or Gradio if available.
"""

import sys
import json
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from .engine import to_natural_banglish, to_natural_codemixed, all_in_one
from .detector import detect_script, get_script_stats
from .normalizer import normalize_text

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🇧🇩 BanglaMultiScript - Live Multi-Script Studio</title>
    <style>
        :root {
            --primary: #006a4e;
            --accent: #f42a41;
            --bg: #f8fafc;
            --card: #ffffff;
            --text: #1e293b;
            --border: #e2e8f0;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
        body { background: var(--bg); color: var(--text); padding: 2rem 1rem; }
        .container { max-width: 900px; margin: 0 auto; }
        header { text-align: center; margin-bottom: 2rem; }
        h1 { font-size: 2.2rem; color: var(--primary); margin-bottom: 0.5rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem; }
        p.subtitle { color: #64748b; font-size: 1.05rem; }
        .card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); margin-bottom: 1.5rem; }
        label { font-weight: 600; display: block; margin-bottom: 0.5rem; color: #334155; }
        textarea { width: 100%; height: 100px; padding: 0.75rem; border: 1.5px solid var(--border); border-radius: 8px; font-size: 1rem; resize: vertical; outline: none; transition: border-color 0.2s; }
        textarea:focus { border-color: var(--primary); }
        .btn-row { display: flex; gap: 0.75rem; margin-top: 1rem; }
        button { background: var(--primary); color: white; border: none; padding: 0.65rem 1.25rem; font-size: 0.95rem; font-weight: 600; border-radius: 6px; cursor: pointer; transition: opacity 0.2s; }
        button:hover { opacity: 0.9; }
        .badge { display: inline-block; padding: 0.25rem 0.6rem; border-radius: 12px; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; background: #e0f2fe; color: #0369a1; }
        .results-grid { display: grid; grid-template-columns: 1fr; gap: 1rem; }
        .output-card { background: #f1f5f9; border: 1px solid var(--border); border-radius: 8px; padding: 1rem; position: relative; }
        .output-card h3 { font-size: 0.9rem; text-transform: uppercase; color: #475569; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center; }
        .output-text { font-size: 1.05rem; line-height: 1.5; color: #0f172a; word-break: break-word; }
        .copy-btn { background: #cbd5e1; color: #1e293b; padding: 0.25rem 0.6rem; font-size: 0.75rem; border-radius: 4px; }
        .copy-btn:hover { background: #94a3b8; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🇧🇩 BanglaMultiScript Studio</h1>
            <p class="subtitle">High-Throughput Bengali to Natural Avro Banglish & Modern Urban Code-Mixed Engine</p>
        </header>

        <div class="card">
            <label for="inputText">Enter Bengali or English text:</label>
            <textarea id="inputText" placeholder="e.g. টু-ফ্যাক্টর অথেনটিকেশন (2FA) কীভাবে অনলাইন অ্যাকাউন্টের পাসওয়ার্ড রক্ষা করে?">অ্যাপল ইনকর্পোরেটেডের সিইও টিম কুকের সম্পূর্ণ ডিএনএ সিকোয়েন্সিং প্রদান করুন।</textarea>
            <div class="btn-row">
                <button onclick="convertText()">Convert Live ⚡</button>
                <button onclick="cleanText()" style="background: #475569;">Normalize Text 🧹</button>
                <span id="detectedBadge" class="badge" style="align-self: center; margin-left: auto;">Detected: Bengali</span>
            </div>
        </div>

        <div class="results-grid">
            <div class="output-card">
                <h3><span>Avro Banglish (Natural)</span><button class="copy-btn" onclick="copyResult('banglishOut')">Copy</button></h3>
                <div class="output-text" id="banglishOut">Apple Inc-er CEO Tim Cook-er shompurno DNA sequencing prodan korun.</div>
            </div>

            <div class="output-card">
                <h3><span>Urban Code-Mixed (Bengali + English)</span><button class="copy-btn" onclick="copyResult('codemixedOut')">Copy</button></h3>
                <div class="output-text" id="codemixedOut">Apple Inc-এর CEO Tim Cook-এর সম্পূর্ণ DNA সিকোয়েন্সিং প্রদান করুন।</div>
            </div>
        </div>
    </div>

    <script>
        async function convertText() {
            const text = document.getElementById('inputText').value;
            if (!text.trim()) return;
            const res = await fetch('/api/convert', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            });
            const data = await res.json();
            document.getElementById('banglishOut').innerText = data.banglish || '';
            document.getElementById('codemixedOut').innerText = data.codemixed || '';
            document.getElementById('detectedBadge').innerText = 'Detected: ' + data.script;
        }

        async function cleanText() {
            const text = document.getElementById('inputText').value;
            const res = await fetch('/api/normalize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            });
            const data = await res.json();
            document.getElementById('inputText').value = data.normalized;
            convertText();
        }

        function copyResult(id) {
            const txt = document.getElementById(id).innerText;
            navigator.clipboard.writeText(txt);
            alert('Copied to clipboard!');
        }
    </script>
</body>
</html>
"""

class MultiScriptHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(HTML_TEMPLATE.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        try:
            req = json.loads(body)
        except Exception:
            req = {}

        text = req.get('text', '')

        if self.path == '/api/convert':
            detected = detect_script(text)
            banglish = to_natural_banglish(text)
            codemixed = to_natural_codemixed(text)
            resp = {
                "script": detected,
                "banglish": banglish,
                "codemixed": codemixed
            }
        elif self.path == '/api/normalize':
            cleaned = normalize_text(text)
            resp = {"normalized": cleaned}
        else:
            resp = {"error": "Invalid endpoint"}

        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(resp, ensure_ascii=False).encode('utf-8'))

    def log_message(self, format, *args):
        # Suppress noisy standard request logs in terminal
        return

def launch_ui(port: int = 7860, host: str = "127.0.0.1", open_browser: bool = True):
    """
    Launches the BanglaMultiScript Web UI studio locally.
    """
    server_address = (host, port)
    httpd = HTTPServer(server_address, MultiScriptHTTPHandler)
    url = f"http://{host}:{port}/"
    print(f"\n=======================================================")
    print(f"🚀 BanglaMultiScript Web Studio is running at: {url}")
    print(f"Press Ctrl+C to stop the server.")
    print(f"=======================================================\n")
    if open_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping BanglaMultiScript Web Studio.")
        httpd.server_close()
