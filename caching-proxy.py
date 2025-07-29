#!/bin/env python3


from utils.parser import parse_arguments
from utils.url_validator import validate_url


def main():
    args = parse_arguments()

    PORT = args.port
    URL = args.origin

    validate_url(URL)

    print(PORT, URL)

if __name__ == '__main__':
    main()