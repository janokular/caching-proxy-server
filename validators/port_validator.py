import socket


def is_port_open(host: str, port: int):
    '''Validate if port is open for the host'''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        result = s.connect_ex((host, port))

        if result == 0:
            return True
        else:
            print(f'error: Port {port} is not open for the {host}')
            return False
