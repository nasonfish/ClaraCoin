import socket
import threading
import json
import time

from chain import BlockChain, Block, Transaction, Confirmation, BlockChainRequest
from mine_network import shout, recv

TASK_NONE = 0
TASK_MINING = 1
TASK_INTURRUPT = 2

task_lock = threading.Lock()
task = TASK_MINING

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

blockchain = None

transactions = []

class MiningInturrupt(Exception):
    pass

def loop():
    while blockchain is None:
        # waiting for blockchain
        time.sleep(5)
    while True:
        try:
            pack = tuple(transactions)
            next_block = blockchain.add_block(mine_block(blockchain.propose(*pack))) # blocks until mining successful or state change
            print("block mined: {}".format(next_block.serialize()))
            for i in pack:
                transactions.remove(i)  # these have been included already :)
            sock.send(next_block.serialize().encode('ascii') + b'\n')
        except MiningInturrupt:
            pass

def mine_block(block_proposal):
    while task is TASK_MINING:
        success = block_proposal.mine() # will return true if successfully mined. this might be inefficient since we check our task so often (between every hash).
        return block_proposal
    raise MiningInturrupt()

def process_line(line):
    """Threaded: when a block is recieved, verify it here, and then change task accordingly"""
    obj = recv(line)
    if type(obj) is BlockChain:
        print("recieved a blockchain")
        if not obj.verify():
            print("bad blockchain")
            return  # bad blockchain
        print("good blockchain")
        blockchain = obj
    elif type(obj) is Block:
        pass
    elif type(obj) is Transaction:
        transactions.append(obj)
    elif type(obj) is Confirmation:
        pass
    elif type(obj) is BlockChainRequest:
        pass  # shout our blockchain
    else:
        pass  # ignore?

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

def request_blockchain():
    shout(sock, BlockChainRequest())

if __name__ == '__main__':
    sock.connect((HOST, PORT))
    
    Client(sock).start()
    request_blockchain()
    loop()

