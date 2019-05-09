#!/usr/bin/env python3

"""

Pietro, Sunny, Daniel

Our results are as follows:

(TL;DR: transactions 1 and 2 are good. Transaction 3 has an invalid signature.
Transaction 4 is referencing an inflow transaction that doesn't exist.
Transaction 5 is trying to spend more money than it has).


======= Transaction txn1 dump =======
Signature verified successfully!
Inflow 0 Transaction: Money: 10
Total money in: 10
Outflow 0 Transaction: Money 5
Outflow 1 Transaction: Money 5
Total money out: 10


======= Transaction txn2 dump =======
Signature verified successfully!
Inflow 0 Transaction: Money: 10500
Total money in: 10500
Outflow 0 Transaction: Money 10000
Outflow 1 Transaction: Money 500
Total money out: 10500


======= Transaction txn3 dump =======
****SIGNATURE FAILED TO VERIFY****
Inflow 0 Transaction: Money: 6000
Total money in: 6000
Outflow 0 Transaction: Money 5000
Outflow 1 Transaction: Money 1000
Total money out: 6000


======= Transaction txn4 dump =======
Signature verified successfully!
Inflow 0 Transaction: Money: 5000
***AN INFLOW TRANSACTION COULD NOT BE FOUND****
Total money in: 5000
Outflow 0 Transaction: Money 6000
Total money out: 6000
****MONEY AMOUNT DOES NOT MATCH****


======= Transaction txn5 dump =======
Signature verified successfully!
Inflow 0 Transaction: Money: 5000
Inflow 1 Transaction: Money: 10
Total money in: 5010
Outflow 0 Transaction: Money 6000
Total money out: 6000
****MONEY AMOUNT DOES NOT MATCH****

"""

import json

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature

BACKEND = default_backend()

BLOCKS = [] # defined below. bad practice, I know, global variable

def sha256(message):
    digest = hashes.Hash(hashes.SHA256(), BACKEND)
    digest.update(message)
    return digest.finalize().hex()

def verify(signature, data, public_key):
    try:
        ed25519.Ed25519PublicKey.from_public_bytes(public_key).verify(signature, data)
        return True
    except InvalidSignature:
        return False

# def block_orderer():
#     block_hashes = {}
#     prev_blocks = {}
# 
#     """Print out hash of the block, its ID, and the hash of its preivous."""
#     blocks = ['block0', 'block1530', 'block2398', 'block3312', 'block7123']
#     for i in blocks:
#         with open(i, 'rb') as f:
#             f_bytes = f.read()
#             f_hash = sha256(f_bytes)
#             block_hashes[i] = f_hash
#             prev_blocks[i] =  json.loads(f_bytes.decode( "ascii" ))[1]
#     for i in prev_blocks:
#         if prev_blocks[i] == 0:
#             print("block {} is the root".format(i))
#         for j in block_hashes:
#             if prev_blocks[i] == block_hashes[j]:
#                 print("block {} is preceeded by {}".format(i, j))


class Block():
    def __init__(self, name):
        print("Building block {}".format(name))
        self.name = name
        with open(name, 'rb') as f:
            f_bytes = f.read()
            self.hash = sha256(f_bytes)
            self.raw = json.loads(f_bytes.decode( "ascii" ))
            self.magic_number = self.raw[0]
            self.prev_hash = self.raw[1]
            self.transactions = []
            for i in self.raw[2]:
                self.transactions.append(Transaction(data=i))
    def set_prev(self, blocks):
        if self.prev_hash == 0:
            self.prev = None
            return
        for i in blocks:
            if i.hash == self.prev_hash:
                self.prev = i
                return

class Transaction():
    def __init__(self, f_name=None, data=None):
        print("Initializing transaction with filename {} or data {}".format(f_name, data))
        self.f_name = f_name
        self.data = data
        if f_name is not None:
            with open(f_name, 'rb') as f:
                f_bytes = f.read()
                self.txn = json.loads(f_bytes.decode( "ascii" ))
        elif data is not None:
            self.txn = data
        else:
            raise Exception("bad")
        self.txn_hash = sha256(json.dumps(self.txn[1]).encode("ascii"))
        self.verified = self.txn_signature_verified()
        self.inflows = []
        for i in self.txn[1][1]:
            print("Building inflows")
            self.inflows.append(InFlow(self.get_public_key(), *i))
        self.outflows = []
        for i in self.txn[1][2]:
            self.outflows.append(OutFlow(*i))

    def get_public_key(self):
        return self.txn[1][0]

    def txn_signature_verified(self):
        signature = bytes.fromhex(self.txn[0])
        public_key = bytes.fromhex(self.txn[1][0])
        return verify(signature, bytes.fromhex(self.txn_hash), public_key)

    def dump(self):
        print("\n\n======= Transaction {} dump =======".format(self.f_name))
        if self.txn_signature_verified():
            print("Signature verified successfully!")
        else:
            print("****SIGNATURE FAILED TO VERIFY****")
        total_money = 0
        for i in range(len(self.inflows)):
            if self.inflows[i].money == -1:
                print("***AN INFLOW TRANSACTION COULD NOT BE FOUND****")
                break
            print("Inflow {} Transaction: Money: {}".format(i, self.inflows[i].money))
            total_money += self.inflows[i].money
        print("Total money in: {}".format(total_money))
        total_out = 0
        for i in range(len(self.outflows)):
            print("Outflow {} Transaction: Money {}".format(i, self.outflows[i].money))
            total_out += self.outflows[i].money
        print("Total money out: {}".format(total_out))
        if total_money != total_out:
            print("****MONEY AMOUNT DOES NOT MATCH****")

class InFlow():
    def __init__(self, recipient, block_id, txn_id):
        self.txn = None
        if block_id is None or txn_id is None:
            self.txn = None
            #return None
        print("searching for block {}".format(block_id))
        self.money = 0
        for i in BLOCKS:
            if i.hash == block_id:
                self.txn = i.transactions[txn_id]
                for i in self.txn.outflows:
                    if i.recipient == recipient:
                        self.money += i.money
        if self.money == 0:
            #raise Exception("Transaction referenced from previous block but not found.")
            self.money = -1
        if self.txn is None:
            raise Exception("no previous block/transaction found for block {} transaction {}".format(block_id, txn_id))

class OutFlow():
    def __init__(self, coins, recipient):
        self.money = coins
        self.recipient = recipient

BLOCK_FILES = ['block0', 'block2398', 'block1530', 'block3312', 'block7123']
# These are in order, but frankly do not need to be. code for ordering is commented up above
for name in BLOCK_FILES:
   BLOCKS.append(Block(name))
for block in BLOCKS:
    block.set_prev(BLOCKS)

if __name__ == "__main__":
    transaction_names = ['txn1', 'txn2', 'txn3', 'txn4', 'txn5']
    transactions = [Transaction(f_name=name) for name in transaction_names]
    for i in transactions:
        i.dump()

