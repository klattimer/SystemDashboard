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


def broadcast_to_list(broadcast):
    (a,b,c,d) = broadcast.split('.')
    if a == 255:
        raise Exception("Cowardly refusing to generate 4.2 billion IP Addresses")
    a = [a]
    if b == 255:
        raise Exception("Cowardly refusing to generate 16.7 million IP Addresses")
    b = [b]
    if c == 255:
        c = range(1, 255)
    if d == 255:
        d = range(1, 255)
    e = [a, b, c, d]
    def rec_addr(l, p):
        if len(l) == p - 1:
            # End of list
            return

        rec_addr(l, p + 1)
        print (p)

        return (p, l)
    rec_addr(e, 0)

if __name__ == '__main__':
    print (broadcast_to_list("192.168.1.255"))
