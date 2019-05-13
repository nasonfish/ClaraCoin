#!/usr/bin/env python3
import json
import os
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature
from util import sha256, verify

class InFlow():
    def __init__(self, recipient, block_id, txn_id):
        self.block_id = block_id
        self.txn_id = txn_id
        self.txn = None
        if block_id is None or txn_id is None:
            self.txn = None
        self.money = 0
        for i in BLOCKS:
            if i.hash == block_id:
                self.txn = i.transactions[txn_id]
                for i in self.txn.outflows:
                    if i.recipient == recipient:
                        self.money += i.money
        if self.money == 0:
            raise Exception("Transaction referenced from previous block but not found.")
        if self.txn is None:
            raise Exception("no previous block/transaction found for block {} transaction {}".format(block_id, txn_id))

    def get_block_id(self):
        return self.block_id
    def get_txn_id(self):
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
