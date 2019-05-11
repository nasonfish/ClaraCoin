import socket
import threading
import json

TASK_NONE = 0
TASK_MINING = 1
TASK_INTURRUPT = 2

task_lock = threading.Lock()
task = TASK_MINING

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class MiningInturrupt(Exception):
    pass

def loop(starting_block):
    while True:
        #prev_block = end of the current chain
        try:
            next_block = mine_block(starting_block)
            print("block mined: {}".format(next_block.serialize()))
            sock.send(next_block.serialize().encode('ascii') + b'\n')
            starting_block = next_block
        except MiningInturrupt:
            pass
    

def mine_block(block_proposal):
    while task == TASK_MINING:
        if block_proposal.mine(): # will return true if successfully mined. this might be inefficient since we check our task so often (between every hash).
            return block_proposal
    raise MiningInturrupt()



def process_line(line):
    """Threaded: when a block is recieved, verify it here, and then change task accordingly"""
    # convert line to block
    # if bad:
    #     return
    print("recieved line {}".format(line))


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

HOST = 'localhost'
PORT = 1264

class TestBlockProposal:
    def __init__(self):
        pass
    def mine(self):
        return True
    def serialize(self):
        return json.dumps(['hello'])

if __name__ == '__main__':
    sock.connect(('0.0.0.0',1264))

    Client(sock).start()
    loop(TestBlockProposal())

