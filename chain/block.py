import json
import os
from util import sha256
from chain import Transaction


class Block():
    def __init__(self, prev_block, transactions, block_idx, magic_num=None):
        if type(prev_block) == int:
            prev_block = str(prev_block)
        self.prev_block = prev_block  # hex
        self.magic_num = magic_num
        self.transactions = transactions
        self.block_idx = block_idx
        self.merkleroot = self.merkle([ txn.get_hash() for txn in self.transactions ])

    @staticmethod
    def load(obj):
        if type(obj) == str:
            obj = json.loads(obj)
        return Block(obj["prev_block"], [ Transaction.load( txn_dict ) for txn_dict in obj["transactions"] ], obj["block_idx"], obj["magic_num"])

    def serialize(self):
        return { "hash": self.get_hash(),
                             "prev_block": self.prev_block,
                             "magic_num": self.magic_num,
                             "merkleroot": self.merkleroot,
                             "transactions": [txn.serialize() for txn in self.transactions],
                             "block_idx": self.block_idx }

    def get_hash(self):
        if self.prev_block == "0":
            prev_hex = b"0"
        else:
            prev_hex = bytes.fromhex(self.prev_block)
        return sha256( prev_hex + bytes.fromhex(self.magic_num) + bytes.fromhex(self.merkleroot) )

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

    def verify(self, blockchain):
        return False in [txn.verify(blockchain) for txn in self.transactions]

class BlockChain:
    def __init__(self, blocks):
        self.blocks = blocks

    def add_block(self, block):
        try:
            block.verify(self)
        except:
            import traceback
            traceback.print_exc()
            print("Block doesn't verify; do not add to chain")
            return

        self.blocks.append(block)
        return block

    def get_tail(self):
        return self.blocks[-1]

    def verify(self):
        for i in range( len(self.blocks)-1 ):
            # Verify transactions of a block
            if i > 0:
                for txn in self.blocks[i+1].transactions:
                    if not txn.verify(self):
                        return False
            # Check proof of work
            block_id = self.blocks[i].get_hash()
            if block_id != self.blocks[i+1].prev_block:
                return False
        return True

    def serialize(self):
        return [block.serialize() for block in self.blocks]

    def propose(self, *txns):
        print("proposing transactions", txns)
        return BlockProposal(self, self.get_tail(), txns)

    @staticmethod
    def load(data):
        if type(data) == str:
            data = json.loads(data)
        return BlockChain([Block.load(d) for d in data])

class BlockProposal:
    def __init__(self, blockchain, prev_block, transactions):
        self.blockchain = blockchain
        self.prev_block = prev_block
        self.transactions = []
        for txn in transactions:
            if txn.verify(blockchain):
                self.transactions.append(txn)
        # TODO add "invent money" functionality
        if len(self.transactions) == 0:
            raise Exception("Cannot propose an empty block.")

    def serialize(self):
        return json.dumps([self.magic_num, self.prev_block.hash, [txn.serialize for txn in self.transactions]])

    def mine(self):
        # if len(valid_transactions) > 0:
        magic_num = os.urandom(32).hex()
        # def __init__(self, prev_block, transactions, block_idx, magic_num=None):
        new_block = Block(self.prev_block.block_idx, self.transactions, str(int(self.prev_block.block_idx) + 1), magic_num)
        if int(new_block.get_hash(), 16) & 0xFFFF == 0xCCCC:
            return new_block
        return False  # failed. maybe next time

class BlockChainRequest:

    def serialize(self):
        return ''

    @staticmethod
    def load(data):
        return BlockChainRequest()

class Confirmation:
    pass
