from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
import json
import pprint
from util import sha256
from chain import Transaction, Block, OutFlow

import os

def getInitialUser():
    private_key = ed25519.Ed25519PrivateKey.from_private_bytes( bytes.fromhex("1d82897e5881368cac9eb99126cdfca1e0317629dbeaa7280484c5dae81e932b") )
    public_key = ed25519.Ed25519PublicKey.from_public_bytes( bytes.fromhex("75efa6f1fdf1393a5ea815b2b3690293d079df187944f22ec79f3380ef7bd743") )
    txns = [Transaction.build_signed_txn("75efa6f1fdf1393a5ea815b2b3690293d079df187944f22ec79f3380ef7bd743",
                             [],
                             [OutFlow(10000, "75efa6f1fdf1393a5ea815b2b3690293d079df187944f22ec79f3380ef7bd743")],
                             "1d82897e5881368cac9eb99126cdfca1e0317629dbeaa7280484c5dae81e932b")]


    block_obj = Block( b"\x00".hex(), txns, 0 )

    success = False
    while not success:
        magic_num = os.urandom(32).hex()
        block_obj.set_magic_num( magic_num )
        if int(block_obj.get_hash(), 16) & 0xFFFF == 0xCCCC:
            success = True
    print(json.dumps(block_obj.serialize()))

if __name__ == '__main__':
    getInitialUser()
    #main()
