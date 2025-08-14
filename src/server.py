import socket
from urllib.request import Request, urlopen, HTTPError


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

        client_conn.close()

    server_socket.close()


def fetch():
    '''Fetch content'''
    content_from_cache = fetch_from_cache()

    if content_from_cache:
        print('Fetched successfully from cache')
        return content_from_cache
    else:
        print('Not in cache\nFetching from server')
        content_from_server = fetch_from_server()

        if content_from_server:
            save_in_cache()


def fetch_from_cache():
    '''Fetch content from the cache storage'''
    try:
        return None
    except:
        return None


def fetch_from_server():
    '''Fetch content from the origin server'''
    pass


def save_in_cache():
    '''Save content in the cache storage'''
    pass


def clear_cache():
    '''Clear all content inside cache storage'''
    pass
