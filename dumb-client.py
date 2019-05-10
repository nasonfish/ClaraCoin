import socket
import threading

TASK_NONE = 0
TASK_MINING = 1
TASK_INTURRUPT = 2
TASK_SHOUT_BLOCK = 3

task_lock = threading.Lock()
task = TASK_NONE

class MiningInturrupt(Exception):
    pass

def loop():
    while True:
        #prev_block = end of the current chain
        try:
            next_block = mine_block()
            with task_lock:
                task = TASK_SHOUT_BLOCK # TODO how do we get our block into the other thread?
        except MiningInturrupt:
            pass
    

def mine_block():
    # prev_block = ???
    while task_lock == TASK_MINING:
        pass # return a new valid block!
    raise MiningInturrupt()



def process_line(line):
    """Threaded: when a block is recieved, verify it here, and then change task accordingly"""
    # convert line to block
    # if bad:
    #     return
    print("recieved line {}".format(line))
    with task_lock:
        task = TASK_INTURRUPT



class Client(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock

    def run(self):
        packet = b''
        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            packet += data
            if '\n' in packet.decode('ascii'):
                s_packet = packet.decode('ascii')
                lines = s_packet.split('\n')
                for i in lines[:-1]:
                    process_line(i)
                if s_packet.endswith('\n'):
                    packet = b''
                else:
                    packet = lines[-1].encode('ascii')
        self.client.close()
        with lock:
            clients.remove(self)

HOST = 'localhost'
PORT = 1264

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('0.0.0.0',1264))

Client(sock).start()

