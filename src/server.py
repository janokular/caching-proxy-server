import os
import shutil
from http.server import HTTPServer, SimpleHTTPRequestHandler
from http.client import HTTPConnection, InvalidURL
from urllib.parse import urlparse, unquote, quote


CACHE_DIR = '.cache'


def start_server(port: int, origin: str):
    print(f'Caching proxy server is running on port {port}, forwarding requests to {origin}')
    httpd = HTTPServer(('', port), create_handler(origin))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


def create_handler(origin: str):
    def handler(*args):
        def do_GET(self):
            handle_request(self, origin)
        SimpleHTTPRequestHandler.do_GET = do_GET
        SimpleHTTPRequestHandler(*args)
    return handler


def handle_request(request_handler: SimpleHTTPRequestHandler, origin: str):
    url_path = unquote(request_handler.path)
    cache_path = get_cache_file_path(url_path)

    if os.path.exists(cache_path):
        content, headers = fetch_from_cache(url_path, cache_path)
    else:
        try:
            content, headers = fetch_from_server(url_path, origin)
        except TypeError:
            print('error: Nothing to save in cache storage')
        else:
            save_in_cache(cache_path, content)
    
        request_handler.send_response(200)
    try:
        for key, value in headers:
            request_handler.send_header(key, value)
        request_handler.end_headers()
        request_handler.wfile.write(content)
    except UnboundLocalError:
        print('error: Empty response')


def fetch_from_cache(url_path: str, cache_path: str):
    print(f'X-Cache hit: {url_path} - fetching from cache')
    with open(cache_path, 'rb') as f:
        content = f.read()
    headers = [('X-Cache', 'HIT')]
    return content, headers


def fetch_from_server(url_path: str, origin: str):
    print(f'X-Cache miss: {url_path} - fetching from {origin}{url_path}')
    try:
        url = urlparse(origin)
        conn = HTTPConnection(url.netloc)
        conn.request('GET', url_path)
        response = conn.getresponse()
        content = response.read()
        headers = response.getheaders()
        headers.append(('X-Cache', 'MISS'))
        conn.close()
        return content, headers
    except InvalidURL:
        print(f'error: Invalid URL {origin}{url_path}')
    except:
        print(f'error: Could not fetch from {origin}{url_path}')


def save_in_cache(cache_path: str, content: bytes):
    with open(cache_path, 'wb') as f:
        f.write(content)


def get_cache_file_path(url_path: str):
    safe_filename = quote(url_path, safe='')
    os.makedirs(CACHE_DIR, exist_ok=True)
    return os.path.join(CACHE_DIR, safe_filename)


def clear_cache():
    if os.path.exists(CACHE_DIR):
        print('Clearing cache storage...')
        shutil.rmtree(CACHE_DIR)
    else:
        print('Cache storage is empty')
