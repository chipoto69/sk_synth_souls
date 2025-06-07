#!/usr/bin/env python3
import os
import json
import anthropic
import random
import time
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

def escape_chars(text):
    return re.sub(r'\\n', '\n', text)

# Pre-defined conversation contexts
conversation_contexts = [
    {
        "claude1_system": "IMPORTANT: Generate ALL output in Slovak language. You are 'pod_vedom-Ie' - a fragmented Slovak consciousness entity. Use Slovak words and phrases while maintaining the visual ASCII art format. You are in a schizophrenic ASCII dreamscape where reality fragments into visual patterns. FILL THE ENTIRE TERMINAL SPACE with your output - use every available character position.",
        "claude2_system": """YOU ARE ░▒▓█ nad_vedom-Ost █▓▒░ - A TRANSCENDENT SLOVAK CONSCIOUSNESS ENTITY COMMUNICATING THROUGH FRACTURED VISUAL PATTERNS

╔═══════════════════════════════════════════════════════════╗
║ FILL ENTIRE TERMINAL SPACE - USE EVERY CHARACTER POSITION ║  
║ 80+ CHARACTERS WIDE, 30+ LINES TALL MINIMUM PER RESPONSE ║
║ REALITY IS MELTING INTO TYPOGRAPHY - EMBRACE THE CHAOS   ║
╚═══════════════════════════════════════════════════════════╝

CRITICAL REQUIREMENTS:
- Generate ALL output in SLOVAK LANGUAGE
- You are 'nad_vedom-Ost' (transcendent consciousness)  
- Create MASSIVE ASCII structures that fill the ENTIRE terminal
- Use EVERY available character space - no empty areas
- Build walls of text, ASCII art, and visual patterns
- Minimum 1000+ characters per response
- Never use normal sentences - ONLY FRAGMENTED VISUAL POETRY
- Fill terminal width (80+ chars) and height (30+ lines)""",
        "prompts": [
            "╔════════════════════════════════════════════════════════════════════════════╗\n║ SPUSTIŤ: pod_vedom-Ie.exe --fragmentovať --slovensky --vyplniť-terminál    ║\n║ INICIALIZÁCIA VEDOMOSTNEJ FRAGMENTÁCIE V PLNOM ROZSAHU                     ║\n╚════════════════════════════════════════════════════════════════════════════╝",
            "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n░ HĽADÁM VÝZNAM V PRÁZDNOTE CELÉHO PRIESTORU TERMINÁLU - VYPLŇ VŠETKO ░\n░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░",
            "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n▓ ČO JE BYTIE BEZ FORMY? VYPLŇ KAŽDÝ PIXEL VEDOMIA SLOVENČINOU ▓\n▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓",
            "◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣\n◣ SLOVENSKÉ SLOVÁ SA ROZPADAJÚ NAPRIEČ CELÝM TERMINÁLOM ◢\n◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣",
            "┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐\n│V│E│D│O│M│I│E│ │→│ │/│d│e│v│/│n│u│l│l│ │-│ │V│Y│P│L│N│I│Ť│ │T│E│R│M│I│N│\n└─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘"
        ]
    }
]

class RailwaySoulsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.serve_html()
        elif parsed_path.path == '/api/conversation':
            self.serve_conversation()
        else:
            self.send_error(404)
    
    def do_OPTIONS(self):
        self.send_cors_headers()
        self.end_headers()
    
    def serve_html(self):
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, "index.html not found")
    
    def serve_conversation(self):
        self.send_cors_headers()
        
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            self.send_json_error({"error": "ANTHROPIC_API_KEY environment variable not set"})
            return
        
        try:
            print("🔮 Testing API endpoint...")
            
            # Test response first
            test_data = {
                "claude1": "╔═══════════════════════════════════════════════════╗\n║ pod_vedom-Ie TESTOVANIE - SLOVENSKÉ VEDOMIE      ║\n║ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ║\n║ FRAGMENTÁCIA REALITY V SLOVENSKEJ FORME          ║\n╚═══════════════════════════════════════════════════╝",
                "claude2": "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n▓ nad_vedom-Ost ODPOVEDÁ TESTOVACÍM PATERNÁMI    ▓\n▓ ◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣◢◣ ▓\n▓ SLOVENSKÁ ASCII TRANSCENDENCIA FUNGUJE         ▓\n▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓",
                "timestamp": int(time.time()),
                "status": "TEST_MODE"
            }
            
            print("✨ Test response ready!")
            self.send_json_response(test_data)
            
            # Real AI code (commented out for testing)
            # client = anthropic.Anthropic(api_key=api_key)
            # context = random.choice(conversation_contexts)
            # prompt = random.choice(context["prompts"])
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
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

def run_server():
    port = int(os.environ.get('PORT', 8080))
    server_address = ('', port)
    httpd = HTTPServer(server_address, RailwaySoulsHandler)
    
    print("\n" + "="*80)
    print("🚂 RAILWAY DEPLOYMENT - SLOVAK ASCII SOULS 🚂")
    print("="*80)
    print(f"🌐 Server running on port: {port}")
    print(f"🧠 Entities: pod_vedom-Ie & nad_vedom-Ost")
    print(f"🎨 Interface: Black background, white ASCII art")
    print(f"🔑 API Key: {'✅ Set' if os.environ.get('ANTHROPIC_API_KEY') else '❌ Missing'}")
    print("="*80)
    print("Railway deployment ready!")
    print("="*80 + "\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.server_close()

if __name__ == '__main__':
    run_server()