import argparse


def parse_arguments():
    '''Parse arguments needed for the program's logic'''
    parser = argparse.ArgumentParser(description='Caching server that caches responses from other servers')

    parser.add_argument('--port', type=int, help='port on which the caching proxy server will run')
    parser.add_argument('--origin', type=str, help='URL of the server to which the requests will be forwarded')    
    parser.add_argument('--clear-cache', action='store_true', help='clear the cache')

    args = parser.parse_args()

    if args.clear_cache:
        if args.port or args.origin:
            parser.error("--clear-cache cannot be used with --port or --origin")
    else:
        if args.port is None or args.origin is None:
            parser.error("Both --port and --origin must be provided unless using --clear-cache")

    return args
