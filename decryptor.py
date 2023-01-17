from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.fernet import Fernet
import utils
import os

PRIVATE_KEY = b"""
-----BEGIN PRIVATE KEY-----
MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCuu49hIWUsCfD9
pWLyphNs3cGHYkAJRWqfPGjpPOpQ7+QJBlM/eKm7SGJy+PDF5rHIfk8FdP+BH/n6
fv54ZeBvCZI+vRQt9juTRotXezlgPdzFjuIupOrNuHf0OGF4zvGKcweOkJbc/XHm
SCjpEIQ0cx7eFbhu9mM7iNR3+XYYDWwtaw4UH2cfO5xPlOb2sHypOPtwdTwirN2T
d6ti1Vy4LUQ8mk1AZImPT7qt036wLewggubPXJldxKNIKtxmbw0N0m+pcF10iJUw
I/bvavlZrvID98MRmhdMCR0XYRJlg5kE4agPJHQgN5nCXxePvWexBZI1JVjWrfV6
/KI0iXYdAgMBAAECggEAJaDYCWWA7Vktt93CH3mSxNbDirVmj2iOw8BlYlb/KdNj
Uus1Cb3hJWb65oIEDcY2onPK7iSqMkMx2Nc40zIzQQ45W3/p5NT6MubV8o6jhj2E
OdohjMRwmUFAucvbd8HvA67uYW3zQx9kRCBliP1Izye8bbyVNXYjXAqFINoMq7R6
jkGiatvvMlg0wQdeenoGbyxFvWpb8SphHCun2hCxrcTShkUBQ1Y1ZEBNuse/x8Yj
AfLCiDcXeIO/pgvyNlqpj7frnW7KDKgRrjeSt8E+qSieh1X4yjS8h6bKpQ/B6k3C
IaauLHhU6n7wOivvRQMow+uZQOD4WFjM9dOuc2fFkQKBgQDt5xyfQp7BZm5cXTJt
Ml0yuUmBv/8s9A1BSQJiHIKB6BsfOpUj46jEWbr0keKIxP20mB2g/3VNFsk3suea
ohOmglSOwgxr+jh8bG5Smjf/AnKUs6j1SurwwOmlACoNdILr5Xs2GxOL799JZ/xo
miDetZUpvy0izRWd+al09XO/8QKBgQC8BkgJJkTIfT+rMHVk/KkR1r7nv6s9qIVL
f7kVtexD6k3qj/rXA53+37UpT0nfTbK4x9PKEq4PwliMH6JdLJKCIcTcASUcM1sG
HfEcnGnYZmLGYnOKw1B7xFdPIrGyvS0pzXcb5RCkOacleZ0D0thIzhXE2Px5ZmC8
WLa0cHEE7QKBgQCj4PUlfAXSIdZaB9UJxYzPuTU6jOChvcg3taxPm2YHSLUOMRO1
cki6YTlY6fmLz28Y7URTuEW8gbrAhJvoOEejBtpqsJ9P7kDk7OiePB/gqXX2m0AD
IMVwbONFxzQwqpbZGu5iGgq/9c/xSBFmmO2VnK4Q4OGdvHpspSOnLsG6cQKBgQCW
LI4sgJw/ZYoMuM+KsSJ4VQR1JOkofgi4nHK/nGXweJty1TyLrx/qCdMwA1wFNpGg
dDn8E59iht8iS8HqmUcLGN2aum9hbsMsx41kRKllZaFOwiN2mTkXIWJ6mkNDd0Uz
NiAD75izEjkl/VQjUavdunw4lPZSICrzRAfpZkVeoQKBgQCN0oQyim3sJWrbJfmC
AYj6dHNPBbz5LfDTbzpICnnxcdyaJtLbPdDqaGSfPUArvxapB03Chhq3KlwLJxGG
K6Gk7w6T95rtWKPhD3NMBEuDcPyBC4/TYqFpKDL57fCLI61gYIOYhsOeqY/82Npp
G+vQqW/pdMT/1RhmUuXeId7p/Q==
-----END PRIVATE KEY-----
"""

def load_private_key():
    private_key = serialization.load_pem_private_key(
        PRIVATE_KEY,
        password=None,
        backend=default_backend()
    )
    return private_key

def load_encrypted_symmetric_key(keypath):
    with open(keypath, "rb") as f:
        encrypted_key = f.read()
        return encrypted_key

def decrypt_with_private_key(private_key, content):
    decrypted_content = private_key.decrypt(
        content,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_content

def decrypt_file(filepath, fernetobj):
    with open(filepath, "rb") as f:
        content = f.read()
        original_content = fernetobj.decrypt(content)
        original_file = open(filepath.replace(".enc", ""), "wb")
        original_file.write(original_content)
        original_file.close()

def crawl(basedir):
    for path, curdir, files in os.walk(basedir):
        for dir in utils.get_unwanted_directories():
            try:
                curdir.remove(dir)
            except:
                pass
        for file in files:
            filepath = os.path.join(path, file)
            if filepath.endswith(".enc"):
                print(filepath)
                try:
                    decrypt_file(filepath, f)
                    utils.remove_file(filepath)
                except:
                    pass

if __name__ == "__main__":
    privkey = load_private_key()
    symkey = load_encrypted_symmetric_key(utils.get_symkey_filepath())
    symkey = decrypt_with_private_key(privkey, symkey)
    f = Fernet(symkey)
    for dir in utils.get_target_directories():
        crawl(dir)
 