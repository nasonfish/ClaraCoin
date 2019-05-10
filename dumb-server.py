import socket
import threading

lock = threading.Lock()
clients = []

class ServerClient(threading.Thread):
    def __init__(self, client, address):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address

    def run(self):
        with lock:
            clients.append(self)
        while True:
            data = self.client.recv(1024)
            if not data:
                break
            for c in clients:
                c.client.send(data)
        self.client.close()
        lock.acquire()
        clients.remove(self)
        lock.release()

while True: # wait for socket to connect
    # send socket to chatserver and start monitoring
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0',1264))
    s.listen(5)
    while True:
        client, address = s.accept()
        ServerClient(client, address).start()

