from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_keys(private_key_path, public_key_path):
    # 生成私钥
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # 从私钥生成公钥
    public_key = private_key.public_key()

    # 将私钥序列化为PEM格式并保存到文件
    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(private_key_path, 'wb') as f:
        f.write(pem_private_key)

    # 将公钥序列化为PEM格式并保存到文件
    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(public_key_path, 'wb') as f:
        f.write(pem_public_key)

    print(f"Private key saved to {private_key_path}")
    print(f"Public key saved to {public_key_path}")

if __name__ == "__main__":
    private_key_path = "private_key.pem"
    public_key_path = "public_key.pem"
    generate_keys(private_key_path, public_key_path)