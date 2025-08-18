import socket


def is_port_open(host: str, port: int):
    '''Validate if port is open for the host'''
    if port in range(1, 65535):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)

        result = s.connect_ex((host, port))
        s.close()

        print(result)

        if result == 0:
            return True
        else:
            print(f'error: Port {port} is not open for the {host}')
            return False
    else:
        print(f'error: Port {port} is out of range')
        return False
