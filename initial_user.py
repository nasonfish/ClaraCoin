from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

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


if __name__ == '__main__':
    main()
