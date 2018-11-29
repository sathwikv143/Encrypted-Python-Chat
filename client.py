#!/usr/bin/python3

# client script to connect to the server
# Note : please ask server for IP and port address

import socket, getpass
from time import sleep
from os import system
from simplecrypt import encrypt,decrypt


# chat method to start cennecting to server and
# start chatting
def chat(host,port):
	server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # creating socket
	system("clear")
	print("Connecting to server...")
	sleep(5)
	server.connect((host, port))
	print("Connected to server {}:{}".format(host,port))
	name = input("Your name : ") # name to identify your self
	passwd = getpass.getpass("Enter password set by client for encrypted chat : ") # password to encrypt chat msgs
	while True:
		msg = input("Me : ")

		encMsg = encrypt(passwd,(name+" : "+msg)) # encrypting msg
		if msg.lower() == "bye":
			server.send(encMsg) # sending encrypted msg
			server.close()
			exit(0)
		else:
			server.send(encMsg) # sending encrypted msg
		print(decrypt(passwd,server.recv(1024)).decode('utf-8')) # receive msg and decrypt

if __name__ == '__main__':
	print("Ask the seerver maintainer for server IP and port")
	host = input("Enter the server IP : ")
	port = int(input("Enter the port : "))
	try:
		chat(host,port)
	except KeyboardInterrupt:
		print("\nKeyboard Interrupted ! \nBye bye...")
		exit()