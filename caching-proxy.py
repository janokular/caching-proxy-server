#!/bin/env python3


from utils.parser import parse_arguments
from utils.port_validator import is_port_open
from utils.url_validator import is_url_recheable


def main():
    args = parse_arguments()

    PORT = args.port
    URL = args.origin

    if is_port_open(PORT) and is_url_recheable(URL):
        print(PORT, URL)

if __name__ == '__main__':
    main()
