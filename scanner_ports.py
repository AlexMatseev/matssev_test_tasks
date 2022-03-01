import ssl
import socket, ipaddress, threading

max_threads = 50
final = {}


def check_port(ip, port):
    host = (ip, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(2.0)
    if port == 443:
        try:
            connection = socket.create_connection(host)
            final[ip, port] = ['OPEN']
            message = b"HEAD / HTTP/1.1\r\nConnection: close\r\nHost: " + bytes(ip, 'utf-8') + b"\r\n\r\n"
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            socket_sock = context.wrap_socket(sock, server_hostname=ip)
            socket_sock.connect(host)
            socket_sock.send(message)
            info = str(socket_sock.recv(1024), 'utf-8')
            if info.find('Server') != -1:
                server = info[info.find('Server'):].split('\n')[0]
                final[ip, port].append(server)
            connection.close()
        except:
            pass
    else:
        try:
            connection = sock.connect(host)
            final[ip, port] = ['OPEN']
            if port == 80:
                message = b"HEAD / HTTP/1.1\r\nHost: " + bytes(ip, 'utf-8') + b"\r\nAccept: text/html\r\n\r\n"
                sock.sendall(message)
                info = str(sock.recv(1024), 'utf-8')
                if info.find('Server') != -1:
                    server = info[info.find('Server'):].split('\n')[0]
                    final[ip,port].append(server)
            connection.close()
        except:
            pass


ports_list = [80, 443, 22, 21, 25]

for port in ports_list:
    for ip in ipaddress.IPv4Network('192.168.1.0/24'):
        for port in ports_list:
            thread = threading.Thread(target=check_port, args=[str(ip), port])
            thread.start()
            thread.join()

print(final)
