import re
import http.client


URL_PATTERN = '^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$'


def is_url_valid(url: str) -> bool:
    '''Validate HTTP and HTTPS URL structure'''
    if bool(re.search(URL_PATTERN, url)):
        return True
    else:
        print(f'error: Provided URL "{url}" is invalid')
        return False


def get_domain_and_path(url: str) -> tuple[str, str]:
    '''Get domain name and path from the URL'''
    domain, path = '', ''

    if url.startswith('https://'):
        domain = url[8:]
    else:
        domain = url[7:]

    if '/' in domain:
        domain_ending_index = domain.index('/')
        path = domain[domain_ending_index:]
        domain = domain[:domain_ending_index]

    return domain, path


def is_url_recheable(url: str) -> bool:
    '''Validate if URL points to a webpage'''
    if is_url_valid(url):
        domain, path = get_domain_and_path(url)

        if url.startswith('https://'):
            conn = http.client.HTTPSConnection(domain)
        else:
            conn = http.client.HTTPConnection(domain)
        
        conn.request('HEAD', path)
        
        if conn.getresponse().status == 200:
            return True
        else:
            print(f'error: URL "{url}" does not point to any webpage')
            return False
