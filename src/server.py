from http.server import HTTPServer, BaseHTTPRequestHandler


CACHE_DIR = '.cache'


def start_server(port, origin):
    '''Start the caching proxy server'''
    httpd = HTTPServer(('', port), BaseHTTPRequestHandler)
    print(f"Caching proxy server is running on port {port}, forwarding requests to: {origin}")
    httpd.serve_forever()


def fetch():
    ''''''
    pass


def fetch_from_cache():
    ''''''
    pass


def fetch_from_origin():
    ''''''
    pass


def save_in_cache():
    ''''''
    pass


def clear_cache():
    '''Clear the cache storage'''
    print('Clearing cache...')
