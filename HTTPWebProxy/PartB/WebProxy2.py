#!/usr/bin/python
# Author: Paarth Lakhani
# uid: u0936913

from socket import *
import sys 
from urlparse import urlparse 
import re
import multiprocessing as mp

# convert to classes and do exception handling
# bug 1: When one client enters the GET request and presses Enter. When I open the second
# client and issue a GET request and press Enter twice, the request is not passed and processed
# until an 'Enter' is pressed for the first one.

def proxy_server(serverRequest, urlRequest, urlPort):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.connect((urlRequest, urlPort))
    serverSocket.send(serverRequest)
    serverResponse = serverSocket.recv(10000)
    serverCurrent = serverResponse
    while len(serverCurrent) > 0:
        serverCurrent = serverSocket.recv(10000)
        serverResponse = serverResponse + serverCurrent
    return serverResponse

def new_client(connectionSocket):
    requestLine = connectionSocket.recv(1024)
#    print requestLine
    '''
    requestLine = None
    buffer = ""
    data = ""
    while True:
        data = connectionSocket.recv(1024)
        if data is None:
            print 'I am breaking'
            break
        else: # data is None
            print 'Data is: ' , data
            buffer+=data
    '''
    
    #print requestLine
    #print len(requestLine)
   # for i in range(len(requestLine)):
    #    print requestLine[i]
    
    requestSplits = requestLine.split()
    if requestSplits[0] == 'GET':
        serverRequest = ""
        url = requestSplits[1]
        urlParts = urlparse(url)
        urlWithPort = urlParts[1]
        m = re.search(":",urlWithPort)
        if m is None:
            urlRequest = urlWithPort
            urlPort = 80
        else:
            urlRequest = urlWithPort[:m.start()]
            urlPort = int(urlWithPort[m.end():])
        serverRequest = serverRequest + requestSplits[0] + " "
        serverRequest = serverRequest + urlParts[2] + " " + requestSplits[2] + "\r\n"
        serverRequest = serverRequest + "Host: " + urlRequest + "\r\n"
        serverRequest = serverRequest + "Connection: close\r\n\r\n"
        print 'This is the request',serverRequest
        print 'This is the request',urlRequest
        serverResponse = proxy_server(serverRequest, urlRequest, urlPort);
        connectionSocket.send(serverResponse)
    elif requestSplits[0] == 'POST' or requestSplits[0] == 'PUT' or requestSplits[0] == 'HEAD':
        serverResponse = "HTTP/1.0 501 Not Implemented\r\n"
        connectionSocket.send(serverResponse)
    connectionSocket.shutdown(SHUT_RDWR)
    connectionSocket.close()

if __name__ == '__main__':
    # Python script starts here.
    port = int(sys.argv[1])
    proxySocket = socket(AF_INET, SOCK_STREAM)
    proxySocket.bind(('',port))
    proxySocket.listen(100)

    while True:
        connectionSocket, addr = proxySocket.accept()
        # run this on a different process
        #p = mp.Process(target=new_client, args=(connectionSocket,))
        #p.start()
        #p.join()
        new_client(connectionSocket);
