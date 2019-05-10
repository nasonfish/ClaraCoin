import socket
import threading

HOST = 'localhost'
PORT = 1264

sock = socket.socket(socket.AF_INIT, socket.SOCK_STREAM)
sock.connect(('0.0.0.0',1264))

TASK_NONE = 0
TASK_MINING = 1
TASK_INTURRUPT = 2
TASK_SHOUT_BLOCK = 3

task_lock = threading.Lock()
task = TASK_NONE

class MiningInturrupt(Exception):
    pass

def loop():
    try:
        next_block = mine_block()
        with task_lock:
            task = TASK_SHOUT_BLOCK # TODO how do we get our block into the other thread?
    except MiningInturrupt:
        pass

def mine_block():
    while task_lock == TASK_MINING:
        pass # return a new valid block!
    raise MiningInturrupt()



def recv_block(block):
    """Threaded: when a block is recieved, verify it here, and then change task accordingly"""
    # verify block
    # if bad:
    #     return
    with task_lock:
        task = TASK_INTURRUPT
