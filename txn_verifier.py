#!/usr/bin/env python3

import json

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature

BACKEND = default_backend()


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

def printTxn( signed_txn ):
    print( "  Signature: %s" % signed_txn[ 0 ] )
    txn = signed_txn[ 1 ]
    print( "  Public key: %s" % txn[ 0 ] )
    print( "  In-flows:" )
    for flow in txn[ 1 ]:
        print( "    Block ID: %s" % flow[ 0 ] )
        print( "    Txn idx: %d" % flow[ 1 ] )
    print( "  Out-flows:" )
    for flow in txn[ 2 ]:
        print( "    Coins: %d" % flow[ 0 ] )
        print( "    Recipient public key: %s" % flow[ 1 ] )

def printBlock( block ):
    print( "Magic number: %d" % block[ 0 ] )
    print( "Prev block hash: %s" % block[ 1 ] )
    for idx in range( len( block[ 2 ] ) ):
        print( "Transaction %d" % idx )
        printTxn( block[ 2 ][ idx ] )

def main():
    print( "Some darn block:" )
    with open( "block3312", "rb" ) as f:
        printBlock( json.loads( f.read().decode( "ascii" ) ) )
    print( "Some darn transaction:" )
    with open( "txn3", "rb" ) as f:
        printTxn( json.loads( f.read().decode( "ascii" ) ) )

def block_orderer():
    block_hashes = {}
    prev_blocks = {}

    """Print out hash of the block, its ID, and the hash of its preivous."""
    blocks = ['block0', 'block1530', 'block2398', 'block3312', 'block7123']
    for i in blocks:
        with open(i, 'rb') as f:
            f_bytes = f.read()
            f_hash = sha256(f_bytes)
            block_hashes[i] = f_hash
            prev_blocks[i] =  json.loads(f_bytes.decode( "ascii" ))[1]
    for i in prev_blocks:
        if prev_blocks[i] == 0:
            print("block {} is the root".format(i))
        for j in block_hashes:
            if prev_blocks[i] == block_hashes[j]:
                print("block {} is preceeded by {}".format(i, j))

def transaction_checker():
    transaction_hashes = {}
    transactions = ['txn1', 'txn2', 'txn3', 'txn4', 'txn5']
    for i in transactions:
        with open(i, 'rb') as f:
            f_bytes = f.read()
            txn = json.loads(f_bytes.decode( "ascii" ))
            txn_hash = sha256(json.dumps(txn[1]).encode("ascii"))
            txn_verify(i, txn, txn_hash)

def txn_verify(name, txn, txn_hash):
    verify_signature(name, txn, txn_hash)

def verify_signature(name, txn, txn_hash):
    signature = bytes.fromhex(txn[0])
    public_key = bytes.fromhex(txn[1][0])
    if verify(signature, bytes.fromhex(txn_hash), public_key):
        print("verification passed! {}".format(name))
    else:
        print("verification failed! {}".format(name))

if __name__ == "__main__":
    main()
    #block_orderer()
    blocks_in_order = ['block0', 'block2398', 'block1530', 'block3312', 'block7123']
    transaction_checker()

