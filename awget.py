import sys
import os
import random
import getopt
import socket
import pickle
import threading

def main():

	url = None

	# default is chaingang.txt
	chainfile = "chaingang.txt"

	#ignore program name
	argv = sys.argv[1:]

	try:
		opts, args = getopt.getopt(argv, "u:c:")

	except:
		print("input error\nussage: -c [chainfile] -u [url]\nNote: chainfile is optional. default chaingang.txt")
		exit(1)

	for opt, arg in opts:
		if opt in ['-c']:
			chainfile = arg
		elif opt in ['-u']:
			url = arg

	if(url == None):
		print("input error\nussage: -c [chainfile] -u [url]\nNote: chainfile is optional. default chaingang.txt")
		exit(1)

	print("awget:")

	chainlist = readFile(chainfile)

	print(f'   Request: {url}')

	printChainList(chainlist)

	#ignore count
	chainlist = chainlist[1:]

	#find a random ss from the list
	ss = random.choice(chainlist)

	

	createConnection(chainlist, ss, url)

def createConnection(chainlist, ss, URL):
	# address ==> ip, port
	ip, port = ss.split()

	print(f'   next SS is <{ip}, {port}>')

	address = (ip, int(port))

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# update the chainlist
	chainlist.remove(ss)

	#append URL to chainlist, so the ss will know where 2 go
	chainlist.append(URL)

	#pack data using pickle
	payload = pickle.dumps(chainlist)

	unpack = pickle.loads(payload)


	#send a connect request
	sock.connect(address)

	#once the connect request is accpeted,
	# send the URL and chainlist to the ss
	sock.sendall(payload)

	print("   waiting for file...")


	# default
	filename = "index.html"

	if('/' in URL):
		filename = URL.split('/')[-1]


	

	threading.Thread(target=handler, args=(sock,filename)).start()


	print(f'   recieved the file {filename}\n    goodbye!')

	exit(1)



def handler(sock, filename):

	arr = bytearray()

	with open(filename, 'wb') as output:

		while True:

			recv = sock.recv(4096)

			if not recv:
				break

			arr.extend(recv)

		output.write(arr)

	sock.close()







	# once you have the ss, ip, port #, create the socket and fill in its values
def printChainList(chainlist):

	#ignore count
	chainlist = chainlist[1:]
	print("   The chainlist is:")

	for ss in chainlist:
		ip, port = ss.split()

		print(f'   <{ip}, {port}>')

def readFile(chainfile):

	try:
		with open(chainfile, 'r') as f:
			lines = f.readlines()
		lines = [x.strip() for x in lines]
		return lines

	except:
		print(f'The chainfile {chainfile} does not exist!')
		exit(1)


if __name__ == "__main__":
	main()
