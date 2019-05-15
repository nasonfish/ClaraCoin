from chain import InFlow, OutFlow
import socket
import time
import threading
import sys
from mine_network import *

blockchain = None
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def main(blockchain):
    private_key = input("Enter your private key: ")
    print()
    # try:
    #     if(len(private_key) != 64):
    #         raise (ValueError("Incorrect Length of Private key"))
    #     int(private_key, 16)
    # except:
    #     print("Please enter a valid private key")
    #     continue

    user_public_key = input("Enter your public key: ")
    print()
    # try:
    #     if(len(user_public_key) != 64):
    #         raise (ValueError("Incorrect Length of public key"))
    #     int(user_public_key, 16)
    # except:
    #     print("Please enter a valid private key")
    #     continue
    inflows, bal = balance(blockchain, user_public_key)
    print("Your current balance is {}".format(bal))

    recip_public_key = input("Enter public key of recipient: ")
    print()
    # try:
    #     if(len(recip_private_key) != 64):
    #         raise (ValueError("Incorrect Length of Recip key"))
    #     int(recip_private_key, 16)
    # except:
    #     print("Please enter a valid public key")
    #     continue
    amount_spend = input("Enter amount of ClaraCoin to be transferred: ")
    print()
    # try:
    #     if (amount_spend != str(int(amount_spend)) and amount_spend < 1):
    #         raise (ValueError("Entered value isn't positive whole number"))
    #     break
    # except:
    #     print("Please enter a positive, whole number amount")
    #     continue
    return user_public_key, private_key, recip_public_key, int(amount_spend)


def balance(blockchain, public_key):
    """Get all the money associated with a public key within a particular blockchain"""
    inflows = []
    for block in blockchain.blocks:
        for i in range(len(block.transactions)):
            txn = block.transactions[i]
            for outflow in txn.outflows:
                if outflow.recipient == public_key:
                    inflows.append((InFlow(public_key, block.block_idx, i), outflow.coins))
    for block in blockchain.blocks:
        for i in range(len(block.transactions)):
            txn = block.transactions[i]
            for inflow in txn.inflows:
                for accounted in inflows:  # bad searching. oh well. blockchain is slow anyway
                    if accounted[0].txn_idx == inflow.txn_idx and accounted[0].block_id == inflow.block_id:
                        inflows.remove(accounted)
    return [f[0] for f in inflows], sum(b[1] for b in inflows)


# TODO all of these have the blockchain argument. maybe they belong
# in the blockchain class
def build_flows(blockchain, from_public, to_public, amount):
    inflows, total = balance(blockchain, from_public)
    outflows = []
    if total < amount:
        raise Exception("You can't send more money than you own.")
    if total > amount:
        outflows.append(OutFlow(total - amount, from_public))  # send to self
    outflows.append(OutFlow(amount, to_public))  # send to target
    return inflows, outflows


HOST = 'nasonfish.com'
PORT = 1264


def request_blockchain():
    shout(sock, BlockChainRequest())


def process_line(line):
    """Threaded: when a block is recieved, verify it here, and then change task accordingly"""
    obj = recv(line)
    global blockchain
    if type(obj) is BlockChain:
        print("Received a Blockchain; validating...")
        if not obj.verify():
            print("Blockchain failed to validate!")
            return  # bad blockchain
        print("Blockchain validated successfully!")
        blockchain = obj
    if type(obj) is Block:
        request_blockchain()

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
    while True:
        while blockchain is None:
            print("Waiting for valid blockchain...")
            time.sleep(5)
        try:
            public, private, target, amount = main(blockchain)
        except EOFError:
            sys.exit(0)
        inflows, total = balance(blockchain, public)
        inflows, outflows = build_flows(blockchain, public, target, amount)
        txn = Transaction.build_signed_txn(public, inflows, outflows, private)
        shout(sock, txn)
        print("Transaction submitted: {}".format(json.dumps(txn.serialize())))
        blockchain = None
        request_blockchain()
