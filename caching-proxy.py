#!/bin/env python3


from utils.parser import parse_arguments
from utils.url_validator import is_url_recheable
from src.proxy import Proxy


HOST = '127.0.0.1'


def main():
    args = parse_arguments()

    PORT = args.port
    URL = args.origin

    if is_url_recheable(URL):
        proxy = Proxy()
        proxy.run(HOST, PORT)


if __name__ == '__main__':
    main()
