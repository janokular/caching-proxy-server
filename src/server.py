import socket
from urllib.request import Request, urlopen, HTTPError
from utils.url_validator import get_domain_and_path


def start_server(host, port, url):
    '''Start the caching proxy server'''
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))

    server_socket.listen(1)

    print(f'Cache proxy server is listening on http://{host}:{port}')

    while True:
        client_conn, client_addr = server_socket.accept()

        request = client_conn.recv(1024).decode()
        print(request)

        headers = request.split('\n')

        domain, path = get_domain_and_path(url)

        content = fetch(domain, path)

        if content:
            response = 'HTTP/1.0 200 OK\n\n' + content
        else:
            response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found\n'

        client_conn.sendall(response.encode())
        client_conn.close()

    server_socket.close()


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
