#!/usr/bin/python3

# client script to connect to the server
# Note : please ask server for IP and port address

import socket
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
	name = input("Your name :") # name to identify your self

	# uncomment the below line to enable encryption
	# passwd = input("Enter password set by client for encrypted chat : ") # password to encrypt chat msgs
	while True:
		msg = input("Me : ")

		# uncomment the below line to encrypt the message
		# encMsg = encrypt(passwd,(name+" : "+msg)) # encrypting msg
		if msg.lower() == "bye":
			# uncomment the below line to encrypt the message
			# server.send(encMsg) # sending encrypted msg

			# comment the below line if above line is uncommented
			server.send((name+" : "+msg).encode('utf-8'))
			server.close()
			exit(0)
		else:
			# uncomment the below line to send encrypted message
			# server.send(encMsg) # sending encrypted msg

			# comment the below line if above line in uncommented
			server.send((name+" : "+msg).encode('utf-8'))
		# print(decrypt(passwd,server.recv(1024)).decode('utf-8')) # receive msg and decrypt
		print(server.recv(1024).decode('utf-8'))

if __name__ == '__main__':
	print("Ask the seerver maintainer for server IP and port")
	host = input("Enter the host IP : ")
	port = int(input("Enter the port : "))
	try:
		chat(host,port)
	except KeyboardInterrupt:
		print("\nKeyboard Interrupted ! \nBye bye...")
		exit()