# /home/sravya1/K2_Spiral_Learning/asgi_wsgi_adapter.py

def adapter(app):
    """
    Adapt an ASGI application to WSGI.
    This is a very simplified adapter and may not handle all ASGI features.
    """
    def wsgi_app(environ, start_response):
        # Extract path and query from environ
        path = environ.get('PATH_INFO', '')
        query = environ.get('QUERY_STRING', '')

        # Create a minimal scope
        scope = {
            'type': 'http',
            'asgi': {'version': '3.0'},
            'http_version': '1.1',
            'method': environ.get('REQUEST_METHOD', 'GET'),
            'scheme': environ.get('wsgi.url_scheme', 'http'),
            'path': path,
            'query_string': query.encode('utf-8'),
            'headers': [],
        }

        # Extract headers
        for key, value in environ.items():
            if key.startswith('HTTP_'):
                name = key[5:].lower().replace('_', '-')
                scope['headers'].append((name.encode('utf-8'), str(value).encode('utf-8')))

        # Handle body input
        body = environ.get('wsgi.input')
        if body:
            body_data = body.read()
        else:
            body_data = b''

        # Send response placeholder
        status_code = [200]
        headers = [[], []]
        body_chunks = [[]]

        def send(event):
            if event['type'] == 'http.response.start':
                status_code[0] = event.get('status', 200)
                headers[0] = event.get('headers', [])
            elif event['type'] == 'http.response.body':
                body_chunks[0].append(event.get('body', b''))

        # Run the ASGI app in a sync manner
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def run_app():
            await app(scope, receive, send)

        async def receive():
            return {
                'type': 'http.request',
                'body': body_data,
                'more_body': False,
            }

        # Run the ASGI app
        loop.run_until_complete(run_app())

        # Prepare the response
        status_line = f"{status_code[0]} Unknown"
        response_headers = [(k.decode('utf-8'), v.decode('utf-8')) for k, v in headers[0]]

        # Send the response
        start_response(status_line, response_headers)
        return [b''.join(body_chunks[0])]

    return wsgi_app