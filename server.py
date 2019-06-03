#!/usr/bin/python3

# server script to initialize the server with
# internal or external network
# Note : please share the IP Address and Port with the 
# client(s) to start chatting.

import socket, getpass
import sys, os
from os import system, path
from time import sleep
from platform import system as systemos, architecture
from simplecrypt import encrypt,decrypt


# using serveo.net to forward port for external network communication
def runServeo():
	print("Connecting to External network....")
	system('ssh -R 9568:0.0.0.0:9568 serveo.net > /dev/null &')
	sleep(5)
	ip = socket.gethostbyname('serveo.net')
	print("IP: {} \t PORT: 9568".format(ip))
	print("Share the above IP and PORT number with client.")

# checking if user needs to connect through Internal Network or External Network
def InternalExternal():
	mode = input("Chat on Internal or External Network ? (I/E): ")
	if mode.lower() == 'e':
		return True
	elif mode.lower() == 'i':
		return False
	else:
		print("Choose correct option !")
		InternalExternal()

# actual code to chat over the network
# the message sent and received are encoded as 'UTF-8'
# change the 80 line for utilizing number of connections to accept
def chat(host,port):
	server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # creating of socket
	server.bind((host, port)) # binding the host and port
	server.listen(5)
	print("Waiting for connection from the client...")
	client, address = server.accept() #accepting connection form client
	system('clear')
	print('Got connection from : ', address)
	name = input("Your name : ") # name to identify yourself
	# set password to encrypt and decrypt the chat
	passwd = getpass.getpass("Enter password for encrypted chat : ") # password to encrypt chat msgs
	while True:
		print(decrypt(passwd,client.recv(1024)).decode('utf-8')) # decrypt the received encrypted msg
		msg = input("Me : ")
		encMsg = encrypt(passwd,(name+" : "+msg)) # encrypt the msg
		if msg.lower() == "bye":
			client.send(encMsg) # send encrypted msg
			client.close()
			server.close()
			system("pkill -f 'ssh -R 9568:0.0.0.0:9568 serveo.net'")
			exit(0)
		else:
			client.send(encMsg) # send encrypted msg

if __name__ == '__main__':
	host = ''
	if InternalExternal():
		runServeo()
		host = "0.0.0.0"
		port = 9568
	else:
		print("Your local IP/host IP is set to :")
		str(list(str(os.system("hostname -I"))).remove('0'))
		host = input("Enter the host : ")
		port = int(input("Enter the port : "))
	try:
		chat(host,port)
	except KeyboardInterrupt:
		print("\nKeyboard Interrupted ! \nBye bye..")
		system("pkill -f 'ssh -R 9568:0.0.0.0:9568 serveo.net'")
		exit()