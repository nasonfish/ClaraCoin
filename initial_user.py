from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
import json
import pprint
from util import sha256
from transaction import Transaction


def main():
    private_key = ed25519.Ed25519PrivateKey.generate()
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
        )
    print(private_bytes.hex())
    # 1d82897e5881368cac9eb99126cdfca1e0317629dbeaa7280484c5dae81e932b

    public_key = private_key.public_key()
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
        )
    print(public_bytes.hex())
    # 75efa6f1fdf1393a5ea815b2b3690293d079df187944f22ec79f3380ef7bd743

    with open("Blocks_updated/block0.json", 'r') as f:
        block = json.loads( f.read() )
        pprint.pprint(block)
        txn = Transaction.load( block["transactions"][0] )

        # txn = block["transactions"][0]["data"]
        # signature = private_key.sign( json.dumps( txn["body"] ).encode("ascii") )
        # public_key.verify(signature, json.dumps( txn["body"] ).encode("ascii") )
        # block['transactions'][0]["data"]["signature"] = signature.hex()
        # block['transactions'][0]["hash"] = sha256( json.dumps( block['transactions'][0]["data"] ).encode("ascii") )

        block['transactions'][0]["data"]["signature"] = txn.signature
        block['transactions'][0]["data"]["hash"] = txn.get_hash()

        pprint.pprint(block)

        block_obj = Block( 0, [ txn ], 0  )
        block["merkleroot"] = block_obj.merkleroot

        success = False
        while not success:
            magic_num = os.urandom(32).hex()
            block_obj.set_magic_num( magic_num )
            if int(block_obj.get_hash(), 8) & 0xFF == 0x0:
                success = True


        block["hash"] = block_obj.get_hash()
        block["magic_num"] = block_obj.magic_num

        pprint.pprint(block)


if __name__ == '__main__':
    main()
