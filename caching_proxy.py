#!/bin/env python3


from utils.parser import parse_arguments
from src.server import start_server, clear_cache


def main():
    args = parse_arguments()
    
    HOST = '0.0.0.0'
    PORT = int(args.port)
    URL = args.origin

    if args.port and args.origin:
        start_server(HOST, PORT, URL)
    elif args.clear_cache:
        clear_cache()


if __name__ == '__main__':
    main()
