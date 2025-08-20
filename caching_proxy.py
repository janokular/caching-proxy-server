#!/bin/env python3


from utils.parser import parse_arguments
from utils.origin_validator import is_origin_valid
from src.server import start_server, clear_cache


def main():
    args = parse_arguments()
    
    port = args.port
    origin = args.origin

    if port and origin:
        if is_origin_valid(origin):
            start_server(port, origin)
    elif args.clear_cache:
        clear_cache()

if __name__ == '__main__':
    main()
