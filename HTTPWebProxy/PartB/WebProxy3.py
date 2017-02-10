#!/usr/bin/python
# Author: Paarth Lakhani
# uid: u0936913

from socket import *
import sys 
from urlparse import urlparse 
import re
import multiprocessing as mp

def proxy_server(serverRequest, host, urlPort):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.connect((host, urlPort))
    serverSocket.send(serverRequest)
    serverResponse = serverSocket.recv(10000)
    serverCurrent = serverResponse
    while len(serverCurrent) > 0:
        serverCurrent = serverSocket.recv(10000)
        serverResponse = serverResponse + serverCurrent
    serverSocket.close()
    return serverResponse


# browsers send a blank line and then the request
# from telnet, only the request comes in.
# https google
# 

def new_client(connectionSocket):
    entireRequest = connectionSocket.recv(1024)
    print 'In a differnet thread'
    # I am not able to figure this out, about the browser and telnet
    if len(entireRequest) > 0:
        requestSplits = entireRequest.splitlines()
        # First Request Line
        requestLine = requestSplits[0]
        # other headers
        headers = requestSplits[1:len(requestSplits) - 1]
        # 1st index is GET; 2nd index is url; 3rd index is HTTP/1.0
        requestComponents = requestLine.split()
        methodType = requestComponents[0]
        
        if methodType == 'GET':
            httpVersion = requestComponents[2]
            urlComponents = urlparse(requestComponents[1])
            urlPort = urlComponents.port
            host = urlComponents.netloc
            path = urlComponents.path
            if urlPort is None:
                urlPort = 80
            else:
                # change the host name
                m = re.search(":",urlComponents.netloc)
                host = urlComponents.netloc[:m.start()]
            requestLine = ""
            requestLine += methodType + " " + path + " " + httpVersion + "\r\n"
            requestLine += "Host: " + host + "\r\n"
            # appending the headers
            for i in range(len(headers)):
                match = re.search(".:.",headers[i])
                if match is None:
                    serverResponse = "HTTP/1.0 400 Bad Request\r\n"
                    connectionSocket.send(serverResponse)
                    connectionSocket.shutdown(SHUT_RDWR)
                    connectionSocket.close()
                    exit()
                else:
                    headerName = headers[i].split(":")
                    headerNameLower = headerName[0].lower()
                    if headerNameLower!= 'connection' and headerNameLower!= 'host':
                        requestLine += headers[i]+"\r\n"
            requestLine += "Connection: close\r\n\r\n"
            serverResponse = proxy_server(requestLine, host, urlPort);
            connectionSocket.send(serverResponse)
        else:
            serverResponse = "HTTP/1.0 501 Not Implemented\r\n"
            connectionSocket.send(serverResponse)
    connectionSocket.shutdown(SHUT_RDWR)
    connectionSocket.close()

if __name__ == '__main__':
    port = int(sys.argv[1])
    proxySocket = socket(AF_INET, SOCK_STREAM)
    proxySocket.bind(('',port))

    # max: 100 requests
    proxySocket.listen(100)
    processes = []

    while True:
        connectionSocket, addr = proxySocket.accept()
        # run this on a different process
        p = mp.Process(target=new_client, args=(connectionSocket,))
        processes.append(p)
        p.start()
        #new_client(connectionSocket)
'''
while True:
    connectionSocket, addr = proxySocket.accept()
    requestLine = connectionSocket.recv(1024)
    print 'this is a request line',requestLine
    requestSplits = requestLine.splitlines()
    print 'this is the length of line',len(requestSplits)
    print 'these are the splits',requestSplits
    connectionSocket.close()

'''
