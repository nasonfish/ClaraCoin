from chain import Block, BlockChain, InFlow, OutFlow, Transaction
from initial_user import getInitialUser
import socket
import time
import threading
from mine_network import *

blockchain = None
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PUBLIC_USER_ROOT = "75efa6f1fdf1393a5ea815b2b3690293d079df187944f22ec79f3380ef7bd743"
PRIVATE_USER_ROOT = "1d82897e5881368cac9eb99126cdfca1e0317629dbeaa7280484c5dae81e932b"

PUBLIC_USER_OTHER = "ee00e543db3b7b5508821b211151d7cea8187613f25bcf3037bbb38bfa7c4dc7"
PRIVATE_USER_OTHER = "7ed318d6602e38caa1a519efb26662a2ad7aa133fbf13d4ed9d09dfc5b58f9b6"

def userInterface():
    #Check for valid public key
    while True:
        private_key = input("Enter your private key")
        try:
            if(len(private_key) != 64):
                raise (ValueError("Incorrect Length of Private key"))
            int(private_key, 16)
        except:
            print("Please enter a valid private key")
            continue

        user_public_key = input("Enter your private key")
        try:
            if(len(user_public_key) != 64):
                raise (ValueError("Incorrect Length of Private key"))
            int(user_public_key, 16)
        except:
            print("Please enter a valid private key")
            continue

        recip_public_key = input("Enter public key of Recipient")
        try:
            if(len(recip_private_key) != 64):
                raise (ValueError("Incorrect Length of Public key"))
            int(recip_private_key, 16)
        except:
            print("Please enter a valid public key")
            continue
        amount_spend = input("Enter amount of Clara Coin to be transfered")
        try:
            if (amount_spend != str(int(amount_spend)) and amount_spend < 1):
                raise (ValueError("Entered value isn't positive whole number"))
            break
        except:
            print("Please enter a positive, whole number amount")
            continue
    #Create transaction
    inflows, outflows = balance(blockchain, user_public_key, recip_public_key, amount_spend)
    txn = Transaction.build_signed_txn(user_public_key, inflows, outflows, private_key)
    print(txn.serialize())


def balance(blockchain, public_key):
    """Get all the money associated with a public key within a particular blockchain"""
    total = 0
    inflows = []
    for block in blockchain.blocks:
        for i in range(len(block.transactions)):
            txn = block.transactions[i]
            for outflow in txn.outflows:
                if outflow.recipient == public_key:
                    inflows.append(InFlow(public_key, block.block_idx, i))
                    total += outflow.coins
            for inflow in txn.inflows:
                for accounted in inflows:  # bad searching. oh well. blockchain is slow anyway
                    if accounted.txn_id == inflow.txn_id:
                        inflows.remove(accounted)
                        total -= accounted.coins
    return inflows, total

# TODO all of these have the blockchain argument. maybe they belong
# in the blockchain class
def build_flows(blockchain, from_public, to_public, amount):
    inflows, total = balance(blockchain, from_public)
    outflows = []
    if total < amount:
        raise Exception("You can't send more money than you own.")
    if total > amount:
        outflows.append(OutFlow(total-amount, from_public)) # send to self
    outflows.append(OutFlow(amount, to_public)) # send to target
    return inflows, outflows

HOST = 'localhost'
PORT = 1264

def request_blockchain():
    shout(sock, BlockChainRequest())

def process_line(line):
    """Threaded: when a block is recieved, verify it here, and then change task accordingly"""
    obj = recv(line)
    global blockchain
    if type(obj) is BlockChain:
        print("recieved a blockchain")
        if not obj.verify():
            print("bad blockchain")
            return  # bad blockchain
        print("good blockchain")
        blockchain = obj

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


if __name__ == '__main__':
    sock.connect((HOST, PORT))

    Client(sock).start()
    request_blockchain()
    while blockchain is None:
        print("Waiting for valid blockchain...")
        time.sleep(5)
    inflows, total = balance(blockchain, PUBLIC_USER_ROOT)
    inflows, outflows = build_flows(blockchain, PUBLIC_USER_ROOT, PUBLIC_USER_OTHER, 5000)
    txn = Transaction.build_signed_txn(PUBLIC_USER_ROOT, inflows, outflows, PRIVATE_USER_ROOT)
    shout(sock, txn)
