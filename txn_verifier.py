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
    def __init__(self, name=None, prev_hash, magic_num, transactions, block_height):
        self.prev_hash = prev_hash
        self.magic_num = magic_num
        self.transactions = transactions
        self.block_height = block_height
        self.merkleroot = self.merkle([ txn.txn_hash for txn in self.transactions ])
        self.hash = self.hash()


    @classmethod
    def load(self, filename):
        with open(filename, 'rb') as f:
            f_bytes = f.read()
            self.hash = sha256(f_bytes)
            self.raw = json.loads(f_bytes.decode( "ascii" ))
            self.magic_number = self.raw[0]
            self.prev_hash = self.raw[1]
            self.transactions = []
            for i in self.raw[2]:
                self.transactions.append(Transaction(data=i))
            self.merkleroot = self.merkle([ txn.txn_hash for txn in self.transactions ])
            # print("merkleroot: ", self.merkleroot)
            self.block_height = None

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

    def serialize(self):
        return json.dumps([self.hash, self.prev_block.hash, self.magic_num, self.block_height, self.merkleroot, [txn.serialize for txn in self.transactions]])

    def hash(self):
        return sha256( bytes.fromhex(self.prev_hash) + bytes.fromhex(self.magic_num) + bytes.fromhex(self.merkleroot) )

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
        for i in range(len(self.transactions):
            if self.transactions[i].is_spent():
                self.transactions[i] = None

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
        # print("F Name " + str(f_name))
        # print(data)
        # self.
        self.f_name = f_name
        self.data = data
        if f_name is not None:
            with open(f_name, 'rb') as f:
                f_bytes = f.read()
                self.load(json.loads(f_bytes.decode( "ascii" )))
        elif data is not None:
            self.load(data)


    def get_public_key(self):
        #Changed this from 1 to [0]
        # print(self.signature)
        # print("get public key ", self.txn[1][0])
        return self.txn[1][0]

    @classmethod
    def generateTxn(blockchain, people): # TODO: includes self?
        pass
        #return Transaction()



    @classmethod
    def load(data):
        self.txn = data
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

    def is_spent(self, blockchain):
        # for each outflow in this transaction, go through all blocks that were
        # mined later than that which this transaction is included in, and
        # see if there is an inflow pointing back to the outflow
        for outflow in self.outflow:
            if not outflow.is_spent():
                return False
        return True

    def txn_signature_verified(self):
        signature = bytes.fromhex(self.txn[0])
        public_key = bytes.fromhex(self.txn[1][0])
        return verify(signature, bytes.fromhex(self.txn_hash), public_key)

    def double_spends(self, public_key, inFlows):
        for i in BLOCKS:
            #Check for every block
            #Check for every block id in transaction
            if not(i.double_spends(public_key, inFlows.get_blockId(), inFlows.get_txnId())):
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
            if not (self.double_spends(self.get_public_key(), self.inflows[i])):
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
        self.block_id = None
        self.txn_idx = None


    '''Return true if there is a transactions in a block such that an inflow is
    coming from this outflow'''
    def is_spent(self):
        # TODO: ideally, we wouldn't have to go through the whole chain but only those blocks formed after
        # the formation of the block this is in
        for block in BLOCKS:
            for txn in block.transactions:
                if self.recipient == txn.get_public_key():
                    for inflow in txn.inflows:
                        if self.block_id == inflow.block_id and self.txn_idx == inflow.txn_idx:
                            return True
        return False


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


BLOCK_FILES = ['Blocks/block0', 'Blocks/block2398', 'Blocks/block1530', 'Blocks/block3312', 'Blocks/block7123']
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


# chain = BLOCKS

if __name__ == '__main__':
    """TESTS / Our homework assignment."""
    BLOCK_FILES = ['BLocks/block0', 'BLocks/block2398', 'BLocks/block1530', 'BLocks/block3312', 'BLocks/block7123']
    # These are in order, but frankly do not need to be. code for ordering is commented up above
    for filename in BLOCK_FILES:
        BLOCKS.append( Block.load(filename) )

    for block in BLOCKS:
        block.set_prev(BLOCKS)

def add_to_chain(block):
    return
    # do verification, add to our list

def mine(*txns):
    """return a block"""
    # pack this list of transactions into a block, verify them, and mine the block


class Person:
    def __init__(self):
        self.public_key = 12345
        self.private_key = 12446

    def makeTransaction(self):

    def mine(self, prev_block, transactions):
        valid_transactions = []
        for txn in transactions:
            if txn.verify():
                valid_transactions.append(txn)

        success = False
        while not success:
            nonce = os.urandom(32).hex()
            new_block = Block(prev_hash, nonce, valid_transactions)
            hsh = sha256( new_block.serialize() )
            if int(hsh, 16) & 0xFFFF == 0x0:
                success = True


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

    def mine(self, prev_block, transactions):
        valid_transactions = []
        for txn in transactions:
            if txn.verify():
                valid_transactions.append(txn)
        if len(valid_transactions) > 0:
            while True:
                magic_num = os.urandom(32).hex()
                new_block = Block(prev_hash, magic_num, valid_transactions, 0)
                if int(new_block.hash, 16) & 0xFFFF == 0x0:
                    return new_block

class BlockChainRequest:

    def serialize():
        return ''

    @classmethod
    def load(data):
        return BlockChainRequest()

