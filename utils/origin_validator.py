import re


ORIGIN_PATTERN = r'^(https?):\/\/([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'


def is_origin_valid(origin: str):
    if bool(re.search(ORIGIN_PATTERN, origin)):
        return True
    else:
        print(f'error: Origin {origin} is invalid')
        return False
