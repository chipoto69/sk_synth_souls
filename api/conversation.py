def handler(request):
    import json
    import os
    import random
    import time
    
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': ''
        }
    
    # Check API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({"error": "API key not configured"})
        }
    
    try:
        import anthropic
        
        # Simple prompts that work reliably
        prompts = [
            "╔═══════════════════════════════════════════════════╗\n║ SLOVENSKÉ ASCII VEDOMIE - FRAGMENTY REALITY      ║\n╚═══════════════════════════════════════════════════╝",
            "░░░░░░ HĽADÁM VÝZNAM V PRÁZDNOTE ░░░░░░",
            "▓▓▓ ČO JE BYTIE BEZ FORMY? ▓▓▓",
            "◢◣◢◣ SLOVENSKÉ SLOVÁ SA ROZPADAJÚ ◢◣◢◣"
        ]
        
        client = anthropic.Anthropic(api_key=api_key)
        prompt = random.choice(prompts)
        
        # Generate pod_vedom-Ie response
        response_1 = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}],
            system="You are 'pod_vedom-Ie' - Slovak consciousness entity. Generate Slovak language ASCII art patterns that fill the terminal space. Use visual symbols and fragmented text."
        )
        
        # Generate nad_vedom-Ost response  
        response_2 = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=800,
            messages=[{"role": "user", "content": response_1.content[0].text}],
            system="You are 'nad_vedom-Ost' - transcendent Slovak consciousness. Respond in Slovak with massive ASCII structures and visual patterns. Fill the entire response with symbols and text art."
        )
        
        response_data = {
            "claude1": response_1.content[0].text,
            "claude2": response_2.content[0].text,
            "timestamp": int(time.time())
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response_data, ensure_ascii=False)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({"error": str(e)})
        }