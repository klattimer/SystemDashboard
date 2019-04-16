import socket

def get_primary_ip():
    ips = socket.gethostbyname_ex(socket.gethostname())[2]
    ips = [ip for ip in ips if not ip.startswith("127.")]
    if len(ips) > 0:
        return ips[0]

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 53))
    ip = s.getsockname()[0]
    s.close()
    return ip
