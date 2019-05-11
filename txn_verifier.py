#!/usr/bin/env python3

"""

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

class Block():
    def __init__(self, name):
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
#<<<<<<< HEAD
#=======
            self.merkleroot = self.merkle([ txn.txn_hash for txn in self.transactions ])
            # print("merkleroot: ", self.merkleroot)


    def set_prev(self, blocks):
        if self.prev_hash == 0:
            self.prev = None
            return
        for i in blocks:
            if i.hash == self.prev_hash:
                self.prev = i
                return

    # TODO Finsih this method
    def check_double_spending(self, public_key, block_id, txn_id):
        #Go through each txn in block
        for txn in self.transactions:
            #check to see if input public key matches
            if (txn.get_public_key() == public_key):
                # Check every inflow of in public key matches
                for inflow in txn.inflows:
                    #If block id and txn id match, then the block double spends
                    if(block_id == inflow.get_blockId() and txn_id == inflow.get_txnId()):
                        return False
        return True

    def merkle( self, hashlist ):

        if len(hashlist) == 0:
            return 0
        elif len(hashlist) == 1:
            return hashlist[0]
        else:
            new_hashlist = []
            for i in range(0, len(hashlist)-1, 2):
                new_hashlist.append( sha256( bytes.fromhex( hashlist[i]) + bytes.fromhex( hashlist[i+1] ) ) )
            if len( hashlist ) % 2 == 1:
                hashlist.append( sha256( hashlist[-1] + hashlist[-1] ) )
            return self.merkle( new_hashlist )

    def prune(self):
        pass


class Transaction():
    def __init__(self, f_name=None, data=None):
        # print("F Name " + str(f_name))
        # print(data)
        # self.
        self.f_name = f_name
        self.data = data
        if f_name is not None:
            with open(f_name, 'rb') as f:
                f_bytes = f.read()
                self.txn = json.loads(f_bytes.decode( "ascii" ))
                printTxn(self.txn)
        elif data is not None:
            self.txn = data
        else:
            raise Exception("bad")


        self.txn_hash = sha256(json.dumps(self.txn[1]).encode("ascii"))
        self.verified = self.txn_signature_verified()
        self.inflows = []
        #Get the inflows

        for i in self.txn[1][1]:
            self.inflows.append(InFlow(self.get_public_key(), *i))
        self.outflows = []

        #Get the Outflows
        for i in self.txn[1][2]:
            self.outflows.append(OutFlow(*i))

    def get_public_key(self):
        #Changed this from 1 to [0]
        # print(self.signature)
        # print("get public key ", self.txn[1][0])
        return self.txn[1][0]

    def txn_signature_verified(self):
        signature = bytes.fromhex(self.txn[0])
        public_key = bytes.fromhex(self.txn[1][0])
        return verify(signature, bytes.fromhex(self.txn_hash), public_key)

    def check_double_spending(self,public_key, inFlows):
        #print("pubKey", str(inFlows.txn.get_public_key()), "blockid",str(inFlows.get_blockId()), "txnID", str(inFlows.get_txnId()))
        for i in BLOCKS:
            #Check for every block
            #Check for every block id in transaction
            if not(i.check_double_spending(public_key, inFlows.get_blockId(), inFlows.get_txnId())):
                print("FALSE")
                return False
        return True


    def verify(self):
        print("\n\n======= Transaction {} dump =======".format(self.f_name))
        if self.txn_signature_verified():
            print("Signature verified successfully!")
        else:
            print("****SIGNATURE FAILED TO VERIFY****")
            return False
        total_money = 0

        for i in range(len(self.inflows)):
            if self.inflows[i].money == -1:
                print("***AN INFLOW TRANSACTION COULD NOT BE FOUND****")
                return False
                break
            print("Inflow {} Transaction: Money: {}".format(i, self.inflows[i].money))
            total_money += self.inflows[i].money

            # Check for Double Spending
            if not (self.check_double_spending(self.get_public_key(),self.inflows[i])):
                print("*** THIS TRANSACTION HAS DOUBLE SPENDING ***")

        print("Total money in: {}".format(total_money))
        total_out = 0

        for i in range(len(self.outflows)):
            print("Outflow {} Transaction: Money {}".format(i, self.outflows[i].money))
            total_out += self.outflows[i].money
        print("Total money out: {}".format(total_out))
        if total_money != total_out:
            print("****MONEY AMOUNT DOES NOT MATCH****")
            return False

class InFlow():
    def __init__(self, recipient, block_id, txn_id):
        # print("BLOCK ID ", block_id)
        # print("txn ID", txn_id)
        self.block_id = block_id
        self.txn_id = txn_id
        self.txn = None
        if block_id is None or txn_id is None:
            self.txn = None
        # print("searching for block {}".format(block_id))
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
    def get_blockId(self):
        return self.block_id
    def get_txnId(self):
        return self.txn_id

class OutFlow():
    def __init__(self, coins, recipient):
        self.money = coins
        self.recipient = recipient

def printTxn( signed_txn ):
	print( "  Signature: %s" % signed_txn[ 0 ] )
	txn = signed_txn[ 1 ]
	print( "  Public key: %s" % txn[ 0 ] )
	print( "  In-flows:" )
	for flow in txn[ 1 ]:
		print( "	Block ID: %s" % flow[ 0 ] )
		print( "	Txn idx: %d" % flow[ 1 ] )
	print( "  Out-flows:" )
	for flow in txn[ 2 ]:
		print( "	Coins: %d" % flow[ 0 ] )
		print( "	Recipient public key: %s" % flow[ 1 ] )


BLOCK_FILES = ['BLocks/block0', 'BLocks/block2398', 'BLocks/block1530', 'BLocks/block3312', 'BLocks/block7123']
# These are in order, but frankly do not need to be. code for ordering is commented up above
for name in BLOCK_FILES:
   BLOCKS.append(Block(name))
for block in BLOCKS:
    block.set_prev(BLOCKS)

if __name__ == "__main__":
    #
    transaction_names = ['Transactions/txn2','Transactions/txn4', 'Transactions/txn1', 'Transactions/txn3', 'Transactions/txn5']
    transactions = [Transaction(f_name=name) for name in transaction_names]
    for i in transactions:
        pass
        #print(i)
        i.verify()


chain = BLOCKS

# TODO

def add_to_chain(block):
    return
    # do verification, add to our list

# <<<<<<< HEAD
def mine(*txns):
    """return a block"""
    # pack this list of transactions into a block, verify them, and mine the block
if __name__ == '__main__':
    """TESTS / Our homework assignment."""
    BLOCK_FILES = ['BLocks/block0', 'BLocks/block2398', 'BLocks/block1530', 'BLocks/block3312', 'BLocks/block7123']
    # These are in order, but frankly do not need to be. code for ordering is commented up above
    for name in BLOCK_FILES:
       BLOCKS.append(Block(name))
    for block in BLOCKS:
        block.set_prev(BLOCKS)


    # if __name__ == "__main__":
    #    transaction_names = ['Transactions/txn2', 'Transactions/txn1', 'Transactions/txn3', 'Transactions/txn4', 'Transactions/txn5']
    #    transactions = [Transaction(f_name=name) for name in transaction_names]
    #    for i in transactions:
            #print(i)
    #        i.verify()


class BlockChain:
    def __init__(self, blocks):
        self.blocks = blocks
    def add_block(self, block):
        # DO ALL THE BLOCK VALIDATION AND REJECT IF UNACCEPTABLE
        self.blocks.append(block)
    def get_tail(self):
        return self.blocks[-1]

class BlockProposal:
    def __init__(self, prev_block, transactions):
        self.transactions = transactions
        self.prev_block = prev_block
    def serialize(self):
        return json.dumps([self.magic_num, self.prev_block.hash, [txn.serialize for txn in self.transactions]])
    def mine(self):
        self.magic_num = os.urandom(32).hex()
        hsh = sha256(self.serialize())
        return int(hsh, 16) & 0xFFFF == 0x0
#>>>>>>> 31d269ef845ff5c52c374d4a6ed743dc8316c8fd
