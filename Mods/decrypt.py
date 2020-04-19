import os
from cryptography.fernet import Fernet
import pickle

class decrpytor:

    def __init__(self, keyfile):
        
        try:
                
            with open(keyfile, 'rb') as file:
                data = file.read()
                file.close()

            data = pickle.loads(data)
            self.key = data['key']
            self.salt = data['salt']
            self.password = data['password']

            self.tool = Fernet(self.key)

            print("Key: ")
            print(self.key)

        except Exception as  e:
            print("error in __init__(): %s" % str(e))
    
    def crypt(self, path):
        try:
            with open(path, 'rb') as file:
                data = file.read()
                file.close()
            
            decrypt_data = self.tool.decrypt(data)

            new_path = path.replace('.crypt', '')
            print(new_path)

            with open(new_path, 'wb') as file:
                file.write(decrypt_data)
                file.close()
            print("decrpyt sucessful!")
            os.remove(path)

        except Exception as e:
            print("error occured in crypt(): %s " %str(e))

keyfile = ''

d = decrpytor('file.key')

def dir_walker():
    extensions = ['.crypt']
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            for ext in extensions:    
                if file.endswith(ext):
                    ally = os.path.join(root, file)
                    print(ally)
                    d.crypt(ally)

dir_walker()