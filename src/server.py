import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from http.client import HTTPConnection
from urllib.parse import urlparse,  unquote, quote


CACHE_DIR = '.cache'
os.makedirs(CACHE_DIR, exist_ok=True)


def start_server(port, origin):
    '''Start the caching proxy server'''
    print(f'Caching proxy server is running on port {port}, forwarding requests to: {origin}')
    httpd = HTTPServer(('', port), create_handler(origin))
    httpd.serve_forever()


def create_handler(origin):
    def handler(*args):
        def do_GET(self):
            handle_request(self, origin)
        SimpleHTTPRequestHandler.do_GET = do_GET
        SimpleHTTPRequestHandler(*args)
    return handler


def handle_request(request_handler, origin):
    origin_path = urlparse(origin)

    path = unquote(request_handler.path)
    cache_file = get_cache_path(path)

    if os.path.exists(cache_file):
        print(f'Cache hit: {path}')
        with open(cache_file, 'rb') as f:
            content = f.read()
        headers = [('Content-Type', 'application/json')]
    else:
        print(f'Cache miss: {path}')
        conn = HTTPConnection(origin_path.netloc)
        conn.request('GET', path)
        response = conn.getresponse()
        content = response.read()
        headers = response.getheaders()
        conn.close()

        with open(cache_file, 'wb') as f:
            f.write(content)

    request_handler.send_response(200)
    for key, value in headers:
        if key.lower() != 'transfer-encoding':
            request_handler.send_header(key, value)
    request_handler.end_headers()
    request_handler.wfile.write(content)


def get_cache_path(path):
    safe_name = quote(path, safe='')
    return os.path.join(CACHE_DIR, safe_name)


def clear_cache():
    '''Clear the cache storage'''
    print('Clearing cache...')
