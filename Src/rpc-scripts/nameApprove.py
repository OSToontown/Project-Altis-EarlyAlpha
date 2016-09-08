#!/usr/bin/python

from jsonrpclib import Server
import time
import random
import json
import math
import os
from Crypto.Cipher import AES
import base64
import sys
import time

RPC_SERVER_SECRET = sys.argv[1]

client = Server(sys.argv[2])

def approveName():
	if raw_input('Enter the users avId: ').startswith('../astron/databases/10000000'):
		f = open(raw_input(),'r')
		filedata = f.read()
		f.close()
	if raw_input() == 'approved':
		newdata = filedata.replace("PENDING","APPROVED")
		f = open(raw_input(),'w')
		f.write(newdata)
		f.close()       
		print 'You just approved a name!'

random.seed()
res = client.ping(approveName(), 12345)
if res != 12345:
	print "Is the server accessable?\n"
	exit

	while True:
		name = client.approveName()
		with open("/var/www/html/api/approval/requests.json", "w") as outfile:
			json.dump(name, outfile)
		print name
		print 'Approved Name!'