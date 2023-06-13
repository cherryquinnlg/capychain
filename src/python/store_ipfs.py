import os

import ipfshttpclient
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hashlib
import base64
import dotenv
# Connect to IPFS client
PASSWORD = os.getenv("ipfs_encryption_password")
IPFS_URL = os.getenv("ipfs_url")



def encrypt_file(input_path, output_path):
    # Read the image file
    with open(input_path, 'rb') as file:
        data = file.read()

    # Generate a random encryption key
    encryption_key = hashlib.sha256(PASSWORD).digest()

    # Create an AES cipher object
    cipher = AES.new(encryption_key, AES.MODE_CBC)

    # Pad the image data
    padded_data = pad(data, AES.block_size)

    # Encrypt the image data
    encrypted_data = cipher.encrypt(padded_data)

    with open(output_path, 'wb') as output_file:
        output_file.write(encrypted_data)


def decrypt_file(input_path, output_path):
    # Generate a 256-bit key from the password
    key = hashlib.sha256(PASSWORD.encode()).digest()

    # Read the encrypted file
    with open(input_path, 'rb') as input_file:
        encrypted_data = input_file.read()

    # Initialize the AES cipher with the key and IV (Initialization Vector)
    cipher = AES.new(key, AES.MODE_ECB)

    # Decrypt the data
    decrypted_data = cipher.decrypt(encrypted_data)

    # Write the decrypted data to the output file
    with open(output_path, 'wb') as output_file:
        output_file.write(decrypted_data)


def store_ipfs(input_path):
    client = ipfshttpclient.connect(IPFS_URL)
    encoded_data = base64.b64encode(encrypted_data)
    res = client.add(encoded_data)

    return res['Hash']
