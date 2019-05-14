import time
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = 'localhost'
PORT = 1264

data = input()

if __name__ == '__main__':
    sock.connect((HOST, PORT))
    sock.send(data.encode('ascii') + b'\n')
    time.sleep(5)
