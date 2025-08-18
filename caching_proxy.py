#!/bin/env python3


from utils.parser import parse_arguments
from validators.origin_validator import is_origin_valid
from validators.port_validator import is_port_open
from src.server import start_server


def main():
    args = parse_arguments()
    
    HOST = '0.0.0.0'
    PORT = args.port
    ORIGIN = args.origin
    CLEAR_CACHE = args.clear_cache

    if PORT and ORIGIN:
        # TODO is_port_open(HOST, PORT)
        if is_origin_valid(ORIGIN):
            start_server(HOST, PORT, ORIGIN)
    elif CLEAR_CACHE:
        print('Clearing cache...')

if __name__ == '__main__':
    main()
