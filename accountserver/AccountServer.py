import os
from socket import *
import thread
import json
import string
import random
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
        self.currconns = []  # We want to keep track of the current connections in order to prevent DoS attacks
        print 'The account server is now running on %s!' % self.host
        self.server()

    #  The server loop
    def server(self):
        while True:
            clientsock, addr = self.serversock.accept()
            print 'Connection from: ', addr
            addr = addr[0]
            self.currconns.append(addr)
            thread.start_new_thread(self.handleClient, (clientsock, addr))

    #  Create a random string that will be used as the key that will encrypt sent and received data
    def cipherkeygen(self, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(8))

    #  Handling the client
    def handleClient(self, clientsock, addr):
        #  Check to see if an IP has multiple connections. Kick the IP if they do.
        conns = 0
        for i in self.currconns:
            if i == addr:
                conns += 1
        if conns > 1:
            print '[SUSPICIOUS] The IP %s has multiple connections! Kicking the client...' % addr
            for i in self.currconns:
                if i == addr:
                    self.currconns.remove(addr)
            clientsock.close()
        else:
            cipherkey = self.cipherkeygen()
            clientsock.send(cipherkey)

            data = clientsock.recv(1024)
            if data == '':
                print '[SUSPICIOUS] Received no data from the client %s!' % (addr)
                clientsock.close()
            else:
                response = self.handleData(data, cipherkey)
                clientsock.send(response)
                clientsock.close()

    #  Encrypt the provided data
    def encrypt(self, data):
        hash_object = hashlib.sha256(data.encode())
        hex_dig = hash_object.hexdigest()
        return hex_dig

    def sendencrypt(self, plaintext, key):
        cipher = XOR.new(key)
        return base64.b64encode(cipher.encrypt(plaintext))

    def senddecrypt(self, ciphertext, key):
        cipher = XOR.new(key)
        return cipher.decrypt(base64.b64decode(ciphertext))

    def handleData(self, data, cipherkey):
        with open(self.cwd + '\\users.json', 'r') as f:
            users = json.load(f)

        data = json.loads(data)  # De-pickle the data using json
        username = ''
        for key, value in data.iteritems():
            username = key
        password = data[username]

        username = self.senddecrypt(str(username), cipherkey)

        if username == 'createaccount' and type(password) is dict:
            for key, value in password.iteritems():
                username = key
            password = password[username]

            username = self.senddecrypt(str(username), cipherkey)
            password = self.senddecrypt(str(password), cipherkey)
            CreateAccount(username, password)
            returndata = json.dumps({str(self.sendencrypt('success', cipherkey)): str(self.sendencrypt('Account created!', cipherkey))})
            return returndata
        else:
            password = self.senddecrypt(str(password), cipherkey)

            if username in users:
                userID = users[username]
                with open(self.cwd + '\\database\\' + str(userID) + '_' + str(username) + '.json', 'r') as f:
                    userDict = json.load(f)
                    if userDict['banned'] == True:
                        error = {str(self.sendencrypt('error', cipherkey)): str(self.sendencrypt('account banned', cipherkey))}
                        return json.dumps(error)
                    else:
                        if userDict['password'] == self.encrypt(password):
                            returndata = json.dumps({str(self.sendencrypt('playcookie', cipherkey)): str(self.sendencrypt(userDict['playcookie'], cipherkey))})
                            return returndata
                        else:
                            error = {str(self.sendencrypt('error', cipherkey)): str(self.sendencrypt('incorrect username/password', cipherkey))}
                            return json.dumps(error)
            else:
                error = {str(self.sendencrypt('error', cipherkey)): str(self.sendencrypt('incorrect username/password', cipherkey))}
                return json.dumps(error)

AccountServer()