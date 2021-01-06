import sys
import random
import os
import getopt
import socket
from _thread import *
import threading
import pickle

def ss(connection, address, port):
    
    # recieve data
    recvd = connection.recv(1024)

    print(f'ss <{address[0]}, {port}>:')
    
    #packed data using pickle
    #so we gotta unpack that bad boy with picke
    
    chain = pickle.loads(recvd)
    # filter out url, that is glommed on the end
    ssonly = chain[:-1]

    # the url is always the last item of the list
    url = chain[-1]

    print(f'   Request: {url}')
    # default
    filename = "index.html"

    #setting the filename
    if('/' in url):
        filename = url.split('/')[-1]

    #if the chain is empty
    if len(ssonly) == 0:

        print("chainlist is empty")

        print(f'issuing wget for file {filename}')

        wget = "wget -q -O " + filename + " " + chain[0]

        os.system(wget)

        sendFile(connection, filename)

        print("   File recieved")
        print("   Relaying file...")
        print("   goodbye!")
              
        
    # chain not empty
    elif len(ssonly) != 0:

        printChainList(ssonly)
        # random choice
        choice = random.choice(ssonly)

        ssonly.remove(choice)

        chain.remove(choice)

        nextss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        ip, port = choice.split()

        print(f'   next ss is <{ip}, {port}>')
       
        address = (ip, int(port))

        nextss.connect(address)

        payload = pickle.dumps(chain)

        nextss.sendall(payload)

        print("   waiting for file...")


        recieveFile(nextss, filename)

        print("   relaying file...")

        sendFile(connection, filename)

        print(f'   Recieved file {filename}')

        print("   goodbye!")


def printChainList(chainList):

    print("   chainlist is: ")

    for item in chainList:
        ip, port = item.split()

        print(f'   <{ip}, {port}>')

def sendFile(socket, filename):

    f = open(filename, 'rb')

    while True:
        l = f.read(1024)

        while(l):
            socket.sendall(l)
            l = f.read(1024)

            if not l:
                f.close()
                socket.close()
                break
        break


def recieveFile(socket, filename):
    with open(filename, 'wb') as output:
        while True:
            # recieve in 1024 bytes
            recv = socket.recv(1024)

            if not recv:
                break

            output.write(recv)




    
def create_socket(hostname, defaultPort = 6666):
    
    print("listening on " + hostname + ", " + str(defaultPort) + "!")
    
    # create socket and fill in its values
    
    ip = socket.gethostbyname(hostname)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    print("Attempting to bind on port " + str(defaultPort) + ".")
    # then bind the socket
    s.bind((ip, int(defaultPort)))
    print("Bind succesfull!")
    
    s.listen(1)

    print("listening...")
    #create a loop statement and set the socket in listen mode
    while(True):
        # set the socket in listen mode
        # accept a connection 
        connection, addr = s.accept()
        
        # create a thread and pass the arguments
        thread = threading.Thread(target=ss, args=(connection,addr,defaultPort, ), daemon=True)
        thread.start()
    
    # close 
    s.close()
         
        
    
def main():

    argv = sys.argv[1:]

    port = None

    try:
        opts, args = getopt.getopt(argv, "p:")

    except:
        print("input error\nussage: -p [port]\nNote: port is optional. defaults to 6666.")
        exit(1)

    for opt, arg in opts:
        if opt in ['-p']:
            port = arg
    
    # if no port provided the default port will be 
    
    if(port == None):
        create_socket(socket.gethostname())
    else:
        create_socket(socket.gethostname(), str(port))

if __name__ == "__main__":
    main()
