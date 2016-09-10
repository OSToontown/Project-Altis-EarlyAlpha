import os
import json
import hashlib
import uuid


class CreateAccount():
    def __init__(self, username, password):
        self.cwd = os.getcwd()

        self.username = username
        self.password = password

        with open(self.cwd + '\\users.json', 'r') as f:
            self.users = json.load(f)
            self.userID = self.users
            self.userID = len(self.userID) + 1
            self.userID = str(self.userID).zfill(7)
            self.users[self.username] = self.userID

        with open(self.cwd + '\\users.json', 'w') as f:
            json.dump(self.users, f, ensure_ascii=True, indent=4, sort_keys=True)

        with open (self.cwd + '\\database\\' + self.userID + '_' + self.username + '.json', 'w') as f:
            self.userData = {'username': self.username,
                             'password': self.encrypt(self.password),
                             'userID': self.userID,
                             'playcookie': self.playcookie(self.username + 'cookie'),
                             'banned': False
                             }
            json.dump(self.userData, f, ensure_ascii=True, indent=4, sort_keys=True)

    def encrypt(self, data):
        hash_object = hashlib.sha256(data.encode())
        hex_dig = hash_object.hexdigest()
        return hex_dig

    def playcookie(self, playcookie):
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + playcookie.encode()).hexdigest()