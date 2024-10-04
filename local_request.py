from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
import requests, argparse, random, base64, os
from dotenv import load_dotenv

load_dotenv()

def load_public_key(public_key_path):
    with open(public_key_path, 'rb') as f:
        pem_public_key = f.read()
        public_key = serialization.load_pem_public_key(
            pem_public_key
        )
    return public_key

def encrypt_with_public_key(public_key, message):
    # 使用公钥加密数据
    encrypted_message = public_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_message

def request_for_image(image, encrypted_message):
    url = f"http://{os.getenv('REMOTE_IP')}:15000/sync_image"
    headers = {"Content-Type": "application/json"}
    data = {"sync_image": image, "encrypted_message": encrypted_message}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        print(response.text)
        raise Exception("Request failed")
    print(response.json())
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send an HTTP request with JSON data.")
    parser.add_argument("--image", help="The docker image wait to sync.")
    args = parser.parse_args()
    public_key_path = "public_key.pem"
    public_key = load_public_key(public_key_path)
    password = os.getenv("PASSWORD")
    salt = random.randint(100000, 999999)
    message = '{"password": "'+password+'", "salt": '+str(salt)+'}'
    encrypted_message = encrypt_with_public_key(public_key, message)
    encrypted_message = base64.b64encode(encrypted_message).decode('utf-8')
    request_for_image(image=args.image, encrypted_message=encrypted_message)