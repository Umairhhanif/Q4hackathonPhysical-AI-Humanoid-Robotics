import os
import json

# Minimal ASGI handler for Vercel
async def app(scope, receive, send):
    if scope['type'] == 'http':
        path = scope['path']
        method = scope['method']
        
        # Health check endpoint
        if path in ['/', '/health'] and method == 'GET':
            env_status = {
                "GOOGLE_API_KEY": "✓" if os.getenv("GOOGLE_API_KEY") else "✗",
                "QDRANT_URL": "✓" if os.getenv("QDRANT_URL") else "✗",
                "QDRANT_API_KEY": "✓" if os.getenv("QDRANT_API_KEY") else "✗",
                "DATABASE_URL": "✓" if os.getenv("DATABASE_URL") else "✗",
                "API_SECRET": "✓" if os.getenv("API_SECRET") else "✗",
            }
            
            response_body = json.dumps({
                "status": "ok",
                "message": "Physical AI RAG Chatbot API",
                "environment_variables": env_status
            }).encode('utf-8')
            
            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': [
                    [b'content-type', b'application/json'],
                    [b'access-control-allow-origin', b'*'],
                ],
            })
            await send({
                'type': 'http.response.body',
                'body': response_body,
            })
            return
        
        # Chat endpoint
        elif path == '/chat' and method == 'POST':
            # Read request body
            body = b''
            while True:
                message = await receive()
                if message['type'] == 'http.request':
                    body += message.get('body', b'')
                    if not message.get('more_body'):
                        break
            
            try:
                request_data = json.loads(body.decode('utf-8'))
                query = request_data.get('query', '')
                
                if not os.getenv("GOOGLE_API_KEY"):
                    error_response = json.dumps({"error": "GOOGLE_API_KEY not configured"}).encode('utf-8')
                    await send({
                        'type': 'http.response.start',
                        'status': 500,
                        'headers': [
                            [b'content-type', b'application/json'],
                            [b'access-control-allow-origin', b'*'],
                        ],
                    })
                    await send({
                        'type': 'http.response.body',
                        'body': error_response,
                    })
                    return
                
                # Import Google Generative AI
                import google.generativeai as genai
                
                genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Start streaming response
                await send({
                    'type': 'http.response.start',
                    'status': 200,
                    'headers': [
                        [b'content-type', b'text/event-stream'],
                        [b'access-control-allow-origin', b'*'],
                        [b'cache-control', b'no-cache'],
                    ],
                })
                
                # Generate response
                system_prompt = """You are an expert assistant for the 'Physical AI & Humanoid Robotics' book.
Answer the user's question helpfully and concisely."""
                
                full_prompt = f"{system_prompt}\n\nQuestion: {query}"
                response = model.generate_content(full_prompt, stream=True)
                
                for chunk in response:
                    if chunk.text:
                        data = json.dumps({'type': 'token', 'data': chunk.text})
                        await send({
                            'type': 'http.response.body',
                            'body': f"data: {data}\n\n".encode('utf-8'),
                            'more_body': True,
                        })
                
                # Send done message
                await send({
                    'type': 'http.response.body',
                    'body': b"data: [DONE]\n\n",
                    'more_body': False,
                })
                
            except Exception as e:
                error_data = json.dumps({'type': 'error', 'data': str(e)})
                await send({
                    'type': 'http.response.body',
                    'body': f"data: {error_data}\n\n".encode('utf-8'),
                    'more_body': False,
                })
            return
        
        # 404 for other paths
        await send({
            'type': 'http.response.start',
            'status': 404,
            'headers': [[b'content-type', b'text/plain']],
        })
        await send({
            'type': 'http.response.body',
            'body': b'Not Found',
        })

# Vercel handler
handler = app
