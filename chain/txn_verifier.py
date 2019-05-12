#!/usr/bin/env python3
import json
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature
from util import sha256

BLOCKS = [] # defined below. bad practice, I know, global variable


def verify(signature, data, public_key):
    try:
        ed25519.Ed25519PublicKey.from_public_bytes(public_key).verify(signature, data)
        return True
    except InvalidSignature:
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
    # TODO
    pass
    # BLOCKS.append(Block(name=name))
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
        pass

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
        try:
            block.verify()
        except:
            print("Block doesn't verify; do not add to chain")
            return

        self.blocks.append(block)

    def get_tail(self):
        return self.blocks[-1]

    def verify(self):
        for i in range( len(blocks)-1 ):
            # Verify transactions of a block
            try:
                self.blocks[i+1].verify()
            except Exception:
                print("Block at position %d failed to verify" % (i+1))
            # Check proof of work
            block_id = self.blocks[i].get_hash()
            if block_id != self.blocks[i+1].prev_hash:
                raise Exception("Previous block id in block at position %d does not match the actual id of previous block" % (i+1))

    def serialize(self):
        return json.dumps(self.blocks)

    def propose(self, *txns):
        return BlockProposal(self.get_tail(), txns)

    @staticmethod
    def load(data):
        return BlockChain(json.loads(data))

class BlockProposal:
    def __init__(self, prev_block, transactions):
        self.prev_block = prev_block
        self.transactions = []
        for txn in transactions:
            if txn.verify():
                self.transactions = transactions.append(txn)
        # TODO add "invent money" functionality

    def serialize(self):
        return json.dumps([self.magic_num, self.prev_block.hash, [txn.serialize for txn in self.transactions]])

    def mine(self):
        # if len(valid_transactions) > 0:
        magic_num = os.urandom(32).hex()
        new_block = Block(prev_hash, magic_num, valid_transactions, 0)
        if int(new_block.hash, 16) & 0xFFFF == 0x0:
            return new_block
        return False # failed. maybe next time

class BlockChainRequest:

    def serialize(self):
        return ''

    @staticmethod
    def load(data):
        return BlockChainRequest()

class Confirmation:
    pass
