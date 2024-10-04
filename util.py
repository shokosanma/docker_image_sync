import os, json, base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from dotenv import load_dotenv

load_dotenv()
def load_private_key(private_key_path):
    with open(private_key_path, 'rb') as f:
        pem_private_key = f.read()
        private_key = serialization.load_pem_private_key(
            pem_private_key,
            password=None
        )
    return private_key

def decrypt_with_private_key(private_key, encrypted_message):
    # 使用私钥解密数据
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_message.decode('utf-8')

def verify(encrypted_message):
    encrypted_message = base64.b64decode(encrypted_message)
    private_key = load_private_key('private_key.pem')
    decrypted_message = decrypt_with_private_key(private_key, encrypted_message)
    # print(decrypted_message, type(decrypted_message))
    passwd = json.loads(decrypted_message)
    # print(passwd)
    return passwd['password'] == os.getenv("PASSWORD")
    
def sync(image, new_image):
    # pull docker image
    print(f"pulling image: {image}")
    os.system(f"docker pull {image}")
    # rename docker image
    print(f"renaming image: {image} to {new_image}")
    os.system(f"docker tag {image} {new_image}")
    # push new docker image
    print(f"pushing image: {new_image}")
    os.system(f"docker push {new_image}")
    # remove old image
    print(f"removing image: {image}")
    os.system(f"docker rmi {image}")
    os.system(f"docker rmi {new_image}")
