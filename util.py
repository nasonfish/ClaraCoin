from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

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
		print( "	Block ID: %s" % flow[ 0 ] )
		print( "	Txn idx: %d" % flow[ 1 ] )
	print( "  Out-flows:" )
	for flow in txn[ 2 ]:
		print( "	Coins: %d" % flow[ 0 ] )
		print( "	Recipient public key: %s" % flow[ 1 ] )


if __name__ == '__main__':
    """TESTS / Our homework assignment."""
    BLOCK_FILES = ['Blocks/block0', 'Blocks/block2398', 'Blocks/block1530', 'Blocks/block3312', 'Blocks/block7123']
    for filename in BLOCK_FILES:
        BLOCKS.append( Block.load(filename) )
    for block in BLOCKS:
        block.set_prev(BLOCKS)

    transaction_names = ['Transactions/txn2','Transactions/txn4', 'Transactions/txn1', 'Transactions/txn3', 'Transactions/txn5']
    transactions = [Transaction(f_name=name) for name in transaction_names]
    for i in transactions:
        pass
        #print(i)
        i.verify()

