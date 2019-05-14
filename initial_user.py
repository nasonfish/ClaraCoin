from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
import json
import pprint
from util import sha256
from chain import Transaction, Block, OutFlow

import os

def main():
    '''
    private_key = ed25519.Ed25519PrivateKey.generate()
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
        )
    print(private_bytes.hex())
    '''
    # 1d82897e5881368cac9eb99126cdfca1e0317629dbeaa7280484c5dae81e932b
    #private_key = ed25519.Ed25519PrivateKey.from_private_bytes( bytes.fromhex("1d82897e5881368cac9eb99126cdfca1e0317629dbeaa7280484c5dae81e932b") )

    '''
    public_key = private_key.public_key()
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
        )
    print(public_bytes.hex())
    '''
    # 75efa6f1fdf1393a5ea815b2b3690293d079df187944f22ec79f3380ef7bd743
    # public_key = ed25519.Ed25519PublicKey.from_public_bytes( bytes.fromhex("75efa6f1fdf1393a5ea815b2b3690293d079df187944f22ec79f3380ef7bd743") )


    # with open("Blocks_updated/block0.json", 'r') as f:
    #     block = json.loads( f.read() )
    #     pprint.pprint(block)
    #     txn = Transaction.load( json.dumps( block["transactions"][0] ) )
    #
    #     # txn = block["transactions"][0]["data"]
    #     # signature = private_key.sign( json.dumps( txn["body"] ).encode("ascii") )
    #     # public_key.verify(signature, json.dumps( txn["body"] ).encode("ascii") )
    #     # block['transactions'][0]["data"]["signature"] = signature.hex()
    #     # block['transactions'][0]["hash"] = sha256( json.dumps( block['transactions'][0]["data"] ).encode("ascii") )
    #
    #     block["transactions"][0]["data"]["signature"] = private_key.sign( json.dumps( block["transactions"][0]["data"]["body"] ).encode("ascii") ).hex( )
    #     block["transactions"][0]["hash"] = txn.get_hash()
    #
    #
    #     block_obj = Block( b"\x00".hex(), [ txn ], 0 )
    #     block["merkleroot"] = block_obj.merkleroot
    #
    #     success = False
    #     while not success:
    #         magic_num = os.urandom(32).hex()
    #         block_obj.set_magic_num( magic_num )
    #         if int(block_obj.get_hash(), 16) & 0xFFFF == 0xCCCC:
    #             success = True
    #
    #
    #     block["hash"] = block_obj.get_hash()
    #     block["magic_num"] = block_obj.magic_num
    block = generateInitialUser()
    pprint.pprint(block)

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
