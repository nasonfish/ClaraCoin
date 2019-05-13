import json
import os
from util import sha256
from chain import Transaction


class Block():
    def __init__(self, prev_block, transactions, block_idx, magic_num=None):
        self.prev_block = prev_block
        self.magic_num = magic_num
        self.transactions = transactions
        print(type(self.transactions[0]))
        self.block_idx = block_idx
        self.merkleroot = self.merkle([ txn.get_hash() for txn in self.transactions ])

    @staticmethod
    def load(obj_str):
        obj_dict = json.loads(obj_str)
        return Block(obj_dict["prev_block"], [ Transaction.load( txn_dict ) for txn_dict in obj_dict["transactions"] ], obj_dict["block_idx"], obj_dict["magic_num"])

    def serialize(self):
        return { "hash": self.get_hash(),
                             "prev_block": self.prev_block,
                             "magic_num": self.magic_num,
                             "merkleroot": self.merkleroot,
                             "transactions": [txn.serialize() for txn in self.transactions],
                             "block_idx": self.block_idx }

    def get_hash(self):
        print( "prev_block type: ", type(self.prev_block), "magic type: ", type(self.magic_num), "merkleroot type: ", type(self.merkleroot))
        return sha256( self.prev_block.encode("ascii") + bytes.fromhex(self.magic_num) + bytes.fromhex(self.merkleroot) )

    def set_magic_num(self, magic_num):
        self.magic_num = magic_num

    def set_prev(self, blocks):
        if self.prev_block == 0:
            self.prev = None
            return
        for i in blocks:
            if i.hash == self.prev_block:
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
        for i in range(len(self.transactions)):
            if self.transactions[i].is_spent():
                self.transactions[i] = None

    def set_prev(self, blocks):
        if self.prev_block == 0:
            self.prev = None
            return
        for i in blocks:
            if i.hash == self.prev_block:
                self.prev = i
                return

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
        for i in range( len(self.blocks)-1 ):
            # Verify transactions of a block
            if i > 0:
                for txn in self.blocks[i+1].transactions:
                    if not txn.verify():
                        return False
            # Check proof of work
            block_id = self.blocks[i].get_hash()
            if block_id != self.blocks[i+1].prev_block:
                return False
        return True

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
        new_block = Block(self.prev_block, magic_num, self.transactions, 0)
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
