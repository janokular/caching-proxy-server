#!/bin/env python3


from utils.parser import parse_arguments
from utils.url_validator import is_url_recheable
from utils.port_validator import is_port_open
from src.server import start_server, clear_cache


def main():
    args = parse_arguments()
    
    HOST = 'localhost'
    PORT = int(args.port)
    URL = str(args.origin)
    CLEAR_CACHE = bool(args.clear_cache)

    if is_port_open(HOST, PORT) and is_url_recheable(URL):
        start_server(HOST, PORT, URL)
    elif CLEAR_CACHE:
        clear_cache()


if __name__ == '__main__':
    main()
