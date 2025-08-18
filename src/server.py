# from http.server import ThreadingHTTPServer


def start_server(host, port, origin):
    '''Start the caching proxy server'''
    # server  = ThreadingHTTPServer(("", port))
    print(f'Cache proxy server is running on http://{host}:{port}, forwarding to {origin}')
    # server.serve_forever()
