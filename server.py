#!/usr/bin/python3

# server script to initialize the server with
# internal or external network
# Note : please share the IP Address and Port with the 
# client(s) to start chatting.

import socket
import sys, os
from os import system, path
from time import sleep
from platform import system as systemos, architecture
from wget import download
from simplecrypt import encrypt,decrypt

# NGROK #
# a port forword-er without need of manipulating the router
# easy to use and work with
# here it is used as to connect to external networks
# for NGROK related error like *authtoken not found*
# go to ngrok.io and create a account and copy authtoken
# run in terminal *./ngrok authtoken <CopiedAuthToken>*

# method to check if the NGROK file exists
def file_exists(file):
	if os.path.exists(file):
		return True
	else:
		return False

# checking ngrok, if not present it will be downloaded
# if already present it runs the ngrok
def checkNgrok():
	if file_exists('ngrok') == False: 
		print('Downloading Ngrok...')
		ostype = systemos().lower()
		if architecture()[0] == '64bit':
			filename = 'ngrok-stable-{0}-amd64.zip'.format(ostype)
		else:
			filename = 'ngrok-stable-{0}-386.zip'.format(ostype)
		url = 'https://bin.equinox.io/c/4VmDzA7iaHb/' + filename
		download(url)
		system('unzip ' + filename)
		system('rm -Rf ' + filename)
		system('clear')
		runNgrok()
	else:
		runNgrok()

# running the downloaded or the already present NGROK file
# over TCP with port 9568 and store it to ngrok.url
def runNgrok():
	system('rm ngrok.url > /dev/null 2>&1')
	system('clear')
	print("Connecting to External network....")
	system('./ngrok tcp 9568 > /dev/null &')
	sleep(10)
	system('curl -s -N http://127.0.0.1:4040/status | grep "tcp://0.tcp.ngrok.io:[0-9]*" -oh > ngrok.url')
	url = open('ngrok.url','r')
	print(url.read())
	print("Share the above URL and PORT number with client.")
	url.close()

# checking if user needs to connect through Internal Network or External Network
def InternalExternal():
	inter = input("Chat on Internal or External Network ? (I/E): ")
	if inter.lower() == 'e':
		return True
	elif inter.lower() == 'i':
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
	name = input("Your name : ") # name to identify youself
	# set password to encrypt and decrypt the chat
	# uncomment bolow line (passwd) to enable encryption password
	# passwd = input("Set password for encrypted chat : ") 
	while True:
		# uncomment below line to receive and decrypt the message
		# print(decrypt(passwd,client.recv(1024)).decode('utf-8')) # decrypt the received encrypted msg
		
		# comment below line if above line is uncommented
		print(client.recv(1024).decode('utf-8'))
		msg = input("Me : ")

		# uncomment the below line to encrypt the message
		#encMsg = encrypt(passwd,(name+" : "+msg)) # encrypt the msg
		if msg.lower() == "bye":
			# uncomment the below line to send encrypted message
			# client.send(encMsg) # send encrypted msg

			# comment the below line if above line in uncommented
			client.send((name+" : "+msg).encode('utf-8'))
			client.close()
			server.close()
			exit(0)
		else:
			# uncomment the below line to send encrypted message
			# client.send(encMsg) # send encrypted msg

			# comment the below line if above line in uncommented
			client.send((name+" : "+msg).encode('utf-8'))

if __name__ == '__main__':
	host = ''
	if InternalExternal():
		checkNgrok()
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
		exit()