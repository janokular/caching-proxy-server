#!/bin/env python3


from utils.parser import parse_arguments
from utils.url_validator import is_url_recheable
from src.server import start_server, clear_cache


HOST = '0.0.0.0'


def main():
    args = parse_arguments()
    
    PORT = int(args.port)
    URL = str(args.origin)

    if PORT and is_url_recheable(URL):
        start_server(HOST, PORT, URL)
    elif args.clear_cache:
        clear_cache()
    else:
        print('error: Something went wrong')


if __name__ == '__main__':
    main()
