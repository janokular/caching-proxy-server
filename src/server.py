import os
import shutil
from http.server import HTTPServer, SimpleHTTPRequestHandler
from http.client import HTTPConnection, InvalidURL
from urllib.parse import urlparse, unquote, quote


CACHE_DIR = '.cache'


def start_server(port: int, origin: str):
    '''Start the caching proxy server'''
    print(f'Caching proxy server is running on port {port}, forwarding requests to {origin}')
    httpd = HTTPServer(('', port), create_handler(origin))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


def create_handler(origin: str):
    '''Create the request handler which injects the origin URL'''
    def handler(*args):
        def do_GET(self):
            handle_get_request(self, origin)
        SimpleHTTPRequestHandler.do_GET = do_GET
        SimpleHTTPRequestHandler(*args)
    return handler


def handle_get_request(request_handler: SimpleHTTPRequestHandler, origin: str):
    '''Process GET request, if possible fetch data from cache storage, otherwise forward to origin server'''
    url_path = unquote(request_handler.path)
    cache_path = get_cache_file_path(url_path)
    content, headers = None, []

    if os.path.exists(cache_path):
        content, headers = fetch_from_cache(url_path, cache_path)
        status_code = 200
    else:
        try:
            content, headers = fetch_from_server(url_path, origin)
            if content is not None:
                save_in_cache(cache_path, content)
                status_code = 200
            else:
                status_code = 502
        except:
            print('error: Nothing to save in cache storage')
            status_code = 502
    
    request_handler.send_response(status_code)
    if content and headers:
        for key, value in headers:
            request_handler.send_header(key, value)
        request_handler.end_headers()
        request_handler.wfile.write(content)


def fetch_from_cache(url_path: str, cache_path: str):
    '''Fetch content from the cache storage'''
    print(f'Cache hit: {url_path} - fetching from cache')
    with open(cache_path, 'rb') as f:
        content = f.read()
    headers = [('X-Cache', 'HIT')]
    return content, headers


def fetch_from_server(url_path: str, origin: str):
    '''Fetch content from the origin server'''
    print(f'Cache miss: {url_path} - fetching from {origin}{url_path}')
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
    except Exception as e:
        print(f'error: Could not fetch from {origin}{url_path} {e}')
    return None, []


def save_in_cache(cache_path: str, content: bytes):
    '''Save content into the cache directory'''
    with open(cache_path, 'wb') as f:
        f.write(content)


def get_cache_file_path(url_path: str):
    '''Generate a safe cache file path from the URL path'''
    safe_filename = quote(url_path, safe='')
    os.makedirs(CACHE_DIR, exist_ok=True)
    return os.path.join(CACHE_DIR, safe_filename)


def clear_cache():
    '''Clear the cache storage'''
    if os.path.exists(CACHE_DIR):
        print('Clearing cache storage...')
        shutil.rmtree(CACHE_DIR)
    else:
        print('Cache storage is empty')
