#!/usr/bin/env python3
import json
import os
from cryptography.exceptions import InvalidSignature
from util import sha256, verifySignature

class InFlow():
    def __init__(self, owner, block_id, txn_idx):
        self.owner = owner
        self.block_id = block_id
        self.txn_idx = txn_idx
        self.txn = None

    def get_block_id(self):
        return self.block_id

    def get_txn_id(self):
        return self.txn_idx

    @staticmethod
    def load(data):
        if type(data) == str:
            data = json.loads(data)
        return InFlow(data["owner"], data['block_id'], data['txn_idx'])

    def serialize(self):
        return {'owner': self.owner, 'block_id': self.block_id, 'txn_idx': self.txn_idx}

class OutFlow():
    def __init__(self, coins, recipient):
        self.coins = coins
        self.recipient = recipient


    @staticmethod
    def load(data):
        if type(data) == str:
            data = json.loads(data)
        return OutFlow(data["number_of_coins"], data['recipient'])
<<<<<<< HEAD

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
=======
>>>>>>> 5e9b9ba9a1d67caaee5d5f31c5a4d9c6b70a045a

    def serialize(self):
        return {'number_of_coins': self.coins, 'recipient': self.recipient}
