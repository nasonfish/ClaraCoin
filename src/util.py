from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature

import json

BACKEND = default_backend()

def sha256(message):
    digest = hashes.Hash(hashes.SHA256(), BACKEND)
    digest.update(message)
    return digest.finalize().hex()


def verifySignature(signature, data, public_key):
    if type(signature) == str:
        signature = bytes.fromhex(signature)
    if type(data) == dict:
        data = json.dumps(data)
    if type(data) == str:
        data = data.encode('ascii')
    if type(public_key) == str:
        public_key = bytes.fromhex(public_key)
    try:
        ed25519.Ed25519PublicKey.from_public_bytes(public_key).verify(signature, data)
        return True
    except InvalidSignature:
        return False


def sign(data, private_key):
    pri_bytes = bytes.fromhex(private_key)
    key = ed25519.Ed25519PrivateKey.from_private_bytes(pri_bytes)
    return key.sign(data.encode('ascii')).hex()
