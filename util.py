from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

BACKEND = default_backend()

def sha256(message):
    digest = hashes.Hash(hashes.SHA256(), BACKEND)
    digest.update(message)
    return digest.finalize().hex()
