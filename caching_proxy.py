#!/bin/env python3


from utils.parser import parse_arguments
from utils.origin_validator import is_origin_valid
from src.server import start_server, clear_cache


def main():
    args = parse_arguments()
    
    PORT = args.port
    ORIGIN = args.origin
    CLEAR_CACHE = args.clear_cache

    if PORT and ORIGIN:
        if is_origin_valid(ORIGIN):
            start_server(PORT, ORIGIN)
    elif CLEAR_CACHE:
        clear_cache()

if __name__ == '__main__':
    main()
