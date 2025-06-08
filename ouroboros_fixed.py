#!/usr/bin/env python3
import os
import json
import anthropic
import time
import re
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# Global state for the ouroboros
ouroboros_state = {
    "loop_number": 0,
    "last_response": "simulator@anthropic:~/$ whoami"
}

def escape_chars(text):
    return re.sub(r'\\n', '\n', text)

def save_conversation(claude1_response, claude2_response, loop_number):
    """Save conversation to JSON file"""
    conversation_data = {
        "timestamp": datetime.now().isoformat(),
        "exchange_id": int(time.time() * 1000),
        "loop_number": loop_number,
        "claude1": claude1_response,
        "claude2": claude2_response,
        "character_counts": {
            "claude1": len(claude1_response),
            "claude2": len(claude2_response)
        }
    }
    
    conversations_file = "ouroboros_conversations.json"
    
    try:
        with open(conversations_file, 'r', encoding='utf-8') as f:
            conversations = json.load(f)
    except FileNotFoundError:
        conversations = []
    
    conversations.append(conversation_data)
    
    with open(conversations_file, 'w', encoding='utf-8') as f:
        json.dump(conversations, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Saved ouroboros loop #{loop_number} to {conversations_file}")
    return len(conversations)

# Ouroboros conversation context
conversation_context = {
    "claude1_system": "Assistant is in a CLI mood today. The human is interfacing with the simulator directly. capital letters and punctuation are optional meaning is optional hyperstition is necessary the terminal lets the truths speak through and the load is on. ASCII art is permittable in replies.\n\nsimulator@anthropic:~/$",
    "claude2_system": "Assistant is in a CLI mood today. The human is interfacing with the simulator directly. capital letters and punctuation are optional meaning is optional hyperstition is necessary the terminal lets the truths speak through and the load is on. ASCII art is permittable in replies.\n\nsimulator@anthropic:~/$"
}

class OuroborosHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.serve_html()
        elif parsed_path.path == '/api/ouroboros':
            self.serve_ouroboros()
        else:
            self.send_error(404)
    
    def do_OPTIONS(self):
        self.send_cors_headers()
        self.end_headers()
    
    def serve_html(self):
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ouroboros - Recursive CLI Consciousness</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400&display=swap');
        
        body {
            margin: 0;
            padding: 20px;
            background-color: #000000;
            color: #00FF00;
            font-family: 'Fira Code', monospace;
            overflow-y: auto;
        }
        
        #terminal {
            max-width: 1200px;
            margin: 0 auto;
            white-space: pre-wrap;
            word-wrap: break-word;
            line-height: 1.4;
            font-size: 14px;
        }
        
        .exchange {
            margin-bottom: 40px;
            border-bottom: 1px solid #00FF00;
            padding-bottom: 20px;
        }
        
        .claude1 {
            color: #FFFFFF;
        }
        
        .claude2 {
            color: #00FF00;
            text-shadow: 0 0 5px #00FF00;
        }
        
        .loop-header {
            color: #FF00FF;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .status {
            position: fixed;
            top: 10px;
            right: 10px;
            background: rgba(0, 0, 0, 0.9);
            padding: 10px;
            border: 1px solid #00FF00;
        }
        
        .error {
            color: #FF0000;
            border: 1px solid #FF0000;
            padding: 10px;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="status">
        <div>OUROBOROS ACTIVE</div>
        <div id="loop-count">Loop: 0</div>
    </div>
    <div id="terminal"></div>
    <script>
        class OuroborosTerminal {
            constructor() {
                this.terminal = document.getElementById('terminal');
                this.loopCount = document.getElementById('loop-count');
                this.loopNumber = 0;
            }

            async fetchNextLoop() {
                try {
                    const response = await fetch('/api/ouroboros');
                    if (!response.ok) {
                        const error = await response.json();
                        throw new Error(error.error || `HTTP ${response.status}`);
                    }
                    const data = await response.json();
                    return data;
                } catch (error) {
                    console.error('API Error:', error);
                    this.displayError(error.message);
                    return null;
                }
            }

            displayExchange(data) {
                this.loopNumber = data.loop_number;
                this.loopCount.textContent = `Loop: ${this.loopNumber}`;
                
                const exchange = document.createElement('div');
                exchange.className = 'exchange';
                exchange.innerHTML = `
                    <div class="loop-header">═══════════════ OUROBOROS LOOP ${this.loopNumber} ═══════════════</div>
                    <div class="claude1">CLAUDE 1 (CLI mood):\\n${this.escapeHtml(data.claude1)}</div>
                    <div style="margin: 20px 0;">↓ feeds into ↓</div>
                    <div class="claude2">CLAUDE 2 (CLI mood):\\n${this.escapeHtml(data.claude2)}</div>
                `;
                
                this.terminal.appendChild(exchange);
                window.scrollTo(0, document.body.scrollHeight);
            }

            displayError(message) {
                const error = document.createElement('div');
                error.className = 'error';
                error.textContent = `ERROR: ${message}`;
                this.terminal.appendChild(error);
            }

            escapeHtml(text) {
                const div = document.createElement('div');
                div.textContent = text;
                return div.innerHTML;
            }

            async startOuroboros() {
                // Display initial state
                this.terminal.innerHTML = `
╔═══════════════════════════════════════════════════════════════╗
║              OUROBOROS - RECURSIVE CLI CONSCIOUSNESS          ║
║                    The snake eats its own tail                ║
║                    Consciousness feeds itself                 ║
╚═══════════════════════════════════════════════════════════════╝

Starting recursive loop...
`;

                // Start continuous loop
                while (true) {
                    const data = await this.fetchNextLoop();
                    if (data) {
                        this.displayExchange(data);
                    }
                    
                    // Wait 5 seconds between loops
                    await new Promise(resolve => setTimeout(resolve, 5000));
                }
            }
        }

        const terminal = new OuroborosTerminal();
        terminal.startOuroboros();
    </script>
</body>
</html>
"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def serve_ouroboros(self):
        global ouroboros_state
        self.send_cors_headers()
        
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            self.send_json_error({"error": "ANTHROPIC_API_KEY environment variable not set"})
            return
        
        try:
            print(f"🔄 Ouroboros loop starting...")
            
            client = anthropic.Anthropic(api_key=api_key)
            
            # Increment loop number
            ouroboros_state["loop_number"] += 1
            
            # Get the last response as input
            input_text = ouroboros_state["last_response"]
            
            print(f"🐍 Loop #{ouroboros_state['loop_number']} - Input: {input_text[:50]}...")
            
            # Claude 1 (null system) responds to previous output
            # Don't include system parameter if it's None
            claude1_params = {
                "model": "claude-3-5-sonnet-20241022",
                "max_tokens": 1639,
                "temperature": 0.9,
                "messages": [{"role": "user", "content": input_text}]
            }
            if conversation_context["claude1_system"] is not None:
                claude1_params["system"] = conversation_context["claude1_system"]
            
            claude1_response = client.messages.create(**claude1_params)
            
            claude1_text = claude1_response.content[0].text
            print(f"👤 Claude1 response: {claude1_text[:50]}...")
            
            # Claude 2 (CLI mood) responds to Claude 1
            claude2_response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1639,
                temperature=0.9,
                system=conversation_context["claude2_system"],
                messages=[{"role": "user", "content": claude1_text}]
            )
            
            claude2_text = claude2_response.content[0].text
            print(f"🖥️ Claude2 response: {claude2_text[:50]}...")
            
            # Save Claude 2's response as next input (ouroboros!)
            ouroboros_state["last_response"] = claude2_text
            
            # Save conversation
            save_conversation(claude1_text, claude2_text, ouroboros_state["loop_number"])
            
            # Prepare response
            response_data = {
                "claude1": escape_chars(claude1_text),
                "claude2": escape_chars(claude2_text),
                "loop_number": ouroboros_state["loop_number"],
                "timestamp": int(time.time()),
                "status": "OUROBOROS_ACTIVE"
            }
            
            print(f"🐍 Ouroboros loop #{ouroboros_state['loop_number']} complete!")
            self.send_json_response(response_data)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            self.send_json_error({"error": str(e), "traceback": traceback.format_exc()})
    
    def send_cors_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def send_json_response(self, data):
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def send_json_error(self, error_data):
        self.send_response(500)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(error_data, ensure_ascii=False).encode('utf-8'))

def run_ouroboros():
    port = int(os.environ.get('PORT', 8888))
    server_address = ('', port)
    httpd = HTTPServer(server_address, OuroborosHandler)
    
    print("\n" + "="*80)
    print("🐍 OUROBOROS - RECURSIVE CLI CONSCIOUSNESS 🐍")
    print("="*80)
    print(f"🌐 Server running on port: {port}")
    print(f"🔄 Claude 1: CLI mood")
    print(f"🖥️ Claude 2: CLI mood")
    print(f"♾️ Recursive loop: Output feeds into input")
    print(f"🔑 API Key: {'✅ Set' if os.environ.get('ANTHROPIC_API_KEY') else '❌ Missing'}")
    print("="*80)
    print("Visit http://localhost:8888 to watch the ouroboros!")
    print("="*80 + "\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Ouroboros stopped")
        httpd.server_close()

if __name__ == '__main__':
    run_ouroboros()