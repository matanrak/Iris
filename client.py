import socket

host = 'localhost'
port = 8021

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.sendall('Hello, world')

data = s.recv(1024)
s.close()

print('Sent....')