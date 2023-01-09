# Demo Python Ransomware 

The following scripts aim to simulate sample ransomware behavior for studying purposes by recursively encrypting files from a specified starting directory.

## Install dependencies

Install dependencies with:
```
python3 -m pip install cryptography
```

## Generate keys

Generate public/private key pair with:

```bash
python3 keygen.py
```
Sample keys are also provided in the repo.

## Building Executables

If you generated a new key pair, edit rans.py and decryptor.py PUBLIC_KEY, PRIVATE_KEY fields respectively.
 
Use [PyInstaller](https://pyinstaller.org/en/stable/installation.html) to build executables for target systems. Install with:

```bash
python3 -m pip install pyinstaller
```

With src directory as the root folder, build the executable (on linux-based or windows hosts) with:
```bash
pyinstaller --onefile rans.py
```
or with:
```bash
python3 -m PyInstaller --onefile ./rans.py
```

Specifically on windows hosts you can force the command prompt to stay in the background with:

```powershell
python -m PyInstaller --onefile .\rans.py
```

## Run Encryptor
Run encrypting process by either running the generated executable or with:
```
python3 rans.py
``` 
In order to avoid further damage, a starting directory is specified. Unless stated otherwise, this demo will start recursively encrypting the included "protected" directory. 

This process will leave behind an encrypted symmetric key. Upon decrypting it with our private key, we can restore the original files.

## Run Decryptor
Run decrypting process with:
```
python3 decryptor.py
``` 
You can also build an executable for this the same way you might built the encrypting process. Note that the encrypted symmetric key left behind by the encrypting process is required in order to restore files.
