import socket
from urllib.request import Request, urlopen, HTTPError
from utils.url_validator import get_domain_and_path


def start_server(host, port, url):
    '''Start the caching proxy server'''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))

    s.listen(1)

    print(f'Cache proxy server is listening on http://{host}:{port}')


def fetch(domain: str, path: str):
    '''Fetch content'''
    content_from_cache = fetch_from_cache(path)

    if content_from_cache:
        print('Fetched successfully from cache')
        return content_from_cache
    else:
        print(f'Not in cache fetching from {domain}')
        content_from_server = fetch_from_server(domain, path)

        if content_from_server:
            save_in_cache()


def fetch_from_cache(path: str):
    '''Fetch content from the cache storage'''
    try:
        return None
    except IOError:
        return None


def fetch_from_server(domain: str, path: str):
    '''Fetch content from the origin server'''
    url = 'http://' + domain + path
    q = Request(url)

    try:
        response = urlopen(q)
        # Grab the header and content from the server req
        response_headers = response.info()
        content = response.read().decode('utf-8')
        return content
    except HTTPError:
        return None


def save_in_cache():
    '''Save content in the cache storage'''
    pass


def clear_cache():
    '''Clear all content inside cache storage'''
    print('Clearing all cache from the cache storage...')
