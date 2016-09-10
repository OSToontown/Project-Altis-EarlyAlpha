import os
from socket import *
import thread
import json
from Crypto.Cipher import XOR
import base64
import hashlib

from CreateAccount import CreateAccount


class AccountServer():
    def __init__(self):
        self.cwd = os.getcwd()

        #  Make required directories and files if they are not there
        if not os.path.isdir(self.cwd + '\\database\\'):
            os.mkdir(self.cwd + '\\database\\')
        if not os.path.isfile(self.cwd + '\\settings.json'):
            defaultsettings = {'ip': '127.0.0.1', 'port': '4014'}
            with open(self.cwd + '\\settings.json', 'w') as f:
                json.dump(defaultsettings, f, ensure_ascii=True, indent=4, sort_keys=True)
        if not os.path.isfile(self.cwd + '\\users.json'):
            defaultusers = {'DEFAULT_USERNAME': '0000001'}
            with open(self.cwd + '\\users.json', 'w') as f:
                json.dump(defaultusers, f, ensure_ascii=True, indent=4, sort_keys=True)
        if not os.path.isfile(self.cwd + '\\database\\0000001_DEFAULT_USERNAME.json'):
            defaultuser = {'username': 'DEFAULT_USERNAME', 'password': self.encrypt('THE_DEFAULT_PASSWORD'),
                           'playcookie': self.encrypt('DEFAULT_USERNAMEcookie'), 'userID': '0000001',
                           'banned': False}
            with open(self.cwd + '\\database\\0000001_DEFAULT_USERNAME.json', 'w') as f:
                json.dump(defaultuser, f, ensure_ascii=True, indent=4, sort_keys=True)

        #  Retrieve the IP and port from the settings file
        with open(self.cwd + '\\settings.json', 'r') as f:
            settings = json.load(f)
            self.host = str(settings['ip'])
            self.port = int(settings['port'])

        #  Create the socket and configure it
        self.serversock = socket(AF_INET, SOCK_STREAM)
        self.serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.serversock.bind((self.host, self.port))
        self.serversock.listen(5)

        #  Start the server!
        self.enabled = True
        print 'The account server is now running!'
        self.server()

    #  The server loop
    def server(self):
        while self.enabled:
            clientsock, addr = self.serversock.accept()
            print 'Connection from:', addr
            thread.start_new_thread(self.handleClient, (clientsock, addr))

    #  Handling the client
    def handleClient(self, clientsock, addr):
        data = clientsock.recv(1024)
        if data == '':
            clientsock.close()
        else:
            response = self.handleData(data)
            clientsock.send(response)
            clientsock.close()

    #  Encrypt the provided data
    def encrypt(self, data):
        hash_object = hashlib.sha256(data.encode())
        hex_dig = hash_object.hexdigest()
        return hex_dig

    def sendencrypt(self, plaintext):
        cipher = XOR.new('iplaypokemongoeveryday')
        return base64.b64encode(cipher.encrypt(plaintext))

    def senddecrypt(self, ciphertext):
        cipher = XOR.new('iplaypokemongoeveryday')
        return cipher.decrypt(base64.b64decode(ciphertext))

    def handleData(self, data):
        with open(self.cwd + '\\users.json', 'r') as f:
            users = json.load(f)

        data = json.loads(data)  # De-pickle the data using json
        username = ''
        for key, value in data.iteritems():
            username = key
        password = data[username]

        username = self.senddecrypt(str(username))

        if username == 'createaccount' and type(password) is dict:
            for key, value in password.iteritems():
                username = key
            password = password[username]

            username = self.senddecrypt(str(username))
            password = self.senddecrypt(str(password))
            CreateAccount(username, password)
            returndata = json.dumps({str(self.sendencrypt('success')): str(self.sendencrypt('Account created!'))})
            return returndata
        else:
            password = self.senddecrypt(str(password))

            if username in users:
                userID = users[username]
                with open(self.cwd + '\\database\\' + str(userID) + '_' + str(username) + '.json', 'r') as f:
                    userDict = json.load(f)
                    if userDict['banned'] == True:
                        error = {str(self.sendencrypt('error')): str(self.sendencrypt('account banned'))}
                        return json.dumps(error)
                    else:
                        if userDict['password'] == self.encrypt(password):
                            returndata = json.dumps({str(self.sendencrypt('playcookie')): str(self.sendencrypt(userDict['playcookie']))})
                            return returndata
                        else:
                            error = {str(self.sendencrypt('error')): str(self.sendencrypt('incorrect username/password'))}
                            return json.dumps(error)
            else:
                error = {str(self.sendencrypt('error')): str(self.sendencrypt('incorrect username/password'))}
                return json.dumps(error)

AccountServer()