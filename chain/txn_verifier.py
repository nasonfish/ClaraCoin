#!/usr/bin/env python3
import json
import os
from cryptography.exceptions import InvalidSignature
from util import sha256, verify

class InFlow():
    def __init__(self, owner, block_id, txn_id):
        self.owner = owner
        self.block_id = block_id
        self.txn_id = txn_id
        self.txn = None

    def get_block_id(self):
        return self.block_id

    def get_txn_id(self):
        return self.txn_id

    @staticmethod
    def load(data):
        if type(data) == str:
            data = json.loads(data)
        return InFlow(data["owner"], data['block_id'], data['txn_id'])

    def serialize(self):
        return {'owner': self.owner, 'block_id': self.block_id, 'txn_id': self.txn_id}

class OutFlow():
    def __init__(self, coins, recipient):
        self.coins = coins
        self.recipient = recipient
        self.block_id = None
        self.txn_idx = None

    @staticmethod
    def load(data):
        if type(data) == str:
            data = json.loads(data)
        return OutFlow(data["number_of_coins"], data['recipient'])

    '''Return true if there is a transaction in a block such that an inflow is
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

    def serialize(self):
        return {'number_of_coins': self.coins, 'recipient': self.recipient}

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
            if int(hsh, 16) & 0xFFFF == 0xCCCC:
                success = True
