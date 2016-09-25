from socket import *
import json
from Crypto.Cipher import XOR
import base64


class TestClient():
    def __init__(self):
        #  Create the socket and configure it
        self.clientsock = socket(AF_INET, SOCK_STREAM)
        self.clientsock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.clientsock.settimeout(5)
        self.clientsock.connect(('127.0.0.1', 4014))
        self.connected = True
        self.client()

    def client(self):
        self.chooseFunc()

        data = self.clientsock.recv(1024)
        self.handle(data)

        self.clientsock.close()

    def chooseFunc(self):
        inpt = raw_input('Login (l) or Create Account (c): ')
        if inpt == 'l':
            username = raw_input('Username: ')
            password = raw_input('Password: ')

            sendData = {str(self.encrypt(username)): str(self.encrypt(password))}
            sendData = json.dumps(sendData)
            self.clientsock.send(sendData)
        elif inpt == 'c':
            username = raw_input('New Username: ')
            password = raw_input('New Password: ')

            sendData = {str(self.encrypt('createaccount')): {str(self.encrypt(username)): str(self.encrypt(password))}}
            sendData = json.dumps(sendData)
            self.clientsock.send(sendData)

    def encrypt(self, plaintext):
        cipher = XOR.new('iplaypokemongoeveryday')
        return base64.b64encode(cipher.encrypt(plaintext))

    def decrypt(self, ciphertext):
        cipher = XOR.new('iplaypokemongoeveryday')
        return cipher.decrypt(base64.b64decode(ciphertext))

    def handle(self, data):
        data = json.loads(data)
        self.key = ''
        for key, value in data.iteritems():
            self.key = key
        self.value = data[self.key]
        self.key = self.decrypt(self.key)
        self.value = self.decrypt(self.value)

        if self.key == 'error':
            print self.key + ': ' + self.value
        elif self.key == 'playcookie':
            print 'launching game!'
        elif self.key == 'success':
            print self.value

TestClient()
