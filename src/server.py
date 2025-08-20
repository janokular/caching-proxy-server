import os
import shutil
from http.server import HTTPServer, SimpleHTTPRequestHandler
from http.client import HTTPConnection
from urllib.parse import urlparse, unquote, quote


CACHE_DIR = '.cache'


def start_server(port: int, origin: str):
    print(f'Caching proxy server is running on port {port}, forwarding requests to {origin}')
    httpd = HTTPServer(('', port), create_handler(origin))
    httpd.serve_forever()


def create_handler(origin: str):
    def handler(*args):
        def do_GET(self):
            handle_request(self, origin)
        SimpleHTTPRequestHandler.do_GET = do_GET
        SimpleHTTPRequestHandler(*args)
    return handler


def handle_request(request_handler: SimpleHTTPRequestHandler, origin: str):
    path = unquote(request_handler.path)
    cache_filename_path = get_cache_path(path)

    if os.path.exists(cache_filename_path):
        print(f'X-Cache hit: {path} - fetched from cache')
        with open(cache_filename_path, 'rb') as f:
            content = f.read()
        headers = [('X-Cache', 'HIT')]
    else:
        print(f'X-Cache miss: {path} - fetching from {origin}{path}')
        origin = urlparse(origin)
        conn = HTTPConnection(origin.netloc)
        conn.request('GET', path)
        response = conn.getresponse()
        content = response.read()
        headers = response.getheaders()
        headers.append(('X-Cache', 'MISS'))
        conn.close()
        with open(cache_filename_path, 'wb') as f:
            f.write(content)

    request_handler.send_response(200)
    for key, value in headers:
        if key.lower() != 'transfer-encoding':
            request_handler.send_header(key, value)
    request_handler.end_headers()
    request_handler.wfile.write(content)


def get_cache_path(path: str):
    safe_filename = quote(path, safe='')
    os.makedirs(CACHE_DIR, exist_ok=True)
    return os.path.join(CACHE_DIR, safe_filename)


def clear_cache():
    print('Clearing cache storage...')
    shutil.rmtree(CACHE_DIR)
