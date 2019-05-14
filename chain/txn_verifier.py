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
        self.money = 0

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

    def serialize(self):
        return {'number_of_coins': self.coins, 'recipient': self.recipient}
