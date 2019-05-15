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
            try:
                data = self.client.recv(1024)
            except Exception:
                break
            print("DATA: {}".format(data))
            if not data:
                break
            for c in clients:
                c.client.send(data)
        self.client.close()
        with lock:
            clients.remove(self)


while True:
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 1264))
    s.listen(5)
    while True:
        client, address = s.accept()
        ServerClient(client, address).start()
