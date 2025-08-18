import re
from http.client import HTTPSConnection, HTTPConnection


ORIGIN_PATTERN = r'^(https?):\/\/([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'


def is_origin_valid(origin: str):
    '''Validate origin URL structure and check if it is reachable'''
    if bool(re.search(ORIGIN_PATTERN, origin)):
        # TODO is_origin_reachable(origin)
        return True
    else:
        print(f'error: "{origin}" is invalid')
        return False


def is_origin_reachable(origin: str):
    '''Validate if origin URL is reachable'''
    if origin.startswith('https://'):
        domain = origin[8:]
        conn = HTTPSConnection(domain)
    else:
        domain = origin[7:]
        conn = HTTPConnection(domain)
    
    conn.request('HEAD', '/')

    if conn.getresponse().status == 200:
        return True
    else:
        print(f'error: "{origin}" is unreachable')
        return False
