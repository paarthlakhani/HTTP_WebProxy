#!/usr/bin/python
# Author: Paarth Lakhani
# uid: u0936913

from socket import *
import sys # Can we use this ?
from urlparse import urlparse # use this ?
# can we use regular expressions
import re

port = int(sys.argv[1])
#port = 2112
proxySocket = socket(AF_INET, SOCK_STREAM)
#proxySocket.bind(('localhost',port))
proxySocket.bind(('',port))

# It should listen to a maximum 100 requests
proxySocket.listen(100)

# proxySocket.accept has a return value which is (conn, address) where conn is a new socket object usable to send and receive data on the connection, and address is the address bound to the socket on the other end of the connection

# Valid request line is: <METHOD><URL><HTTP VERSION>
# All other headers need to properly formatted like:
# <HEADER NAME>: <HEADER VALUE>

# Things that you need to take care:
# Return proper responses back based on the scenarios:
#          anything other than GET
#          If the headers are not in the form __:__ form
# Ip addresses
# Use the port coming from the request. If there is no port given: use default: 80 Progress
# make sure headers are in the correct form of __:__ using regular expressions Progress
# The response has HTTP/1.1

while True:
    connectionSocket, addr = proxySocket.accept()
    requestLine = connectionSocket.recv(1024)
    requestSplits = requestLine.split()
    if requestSplits[0] == 'GET':
        serverRequest = ""
        url = requestSplits[1]
        urlParts = urlparse(url)
        #print urlParts
        urlWithPort = urlParts[1]
        #print urlWithPort
        m = re.search(":",urlWithPort)
        #print urlWithPort
        if m is None:
            # Replace it with appropriate urlRequest and urlPort
            urlRequest = urlWithPort
            urlPort = 80
        else:
            urlRequest = urlWithPort[:m.start()]
            urlPort = int(urlWithPort[m.end():])
        serverRequest = serverRequest + requestSplits[0] + " "
        serverRequest = serverRequest + urlParts[2] + " " + requestSplits[2] + "\r\n"
        serverRequest = serverRequest + "Host: " + urlRequest + "\r\n"
        headers = ""
        while True:
            currentMessage = connectionSocket.recv(1024)
            if currentMessage == '\r\n':
                break;
            else:
                # check here whether there is no header named connection
                match = re.search(".:.",currentMessage)
                #print match
                if match is None:
                    serverResponse = "HTTP/1.0 400 Bad Request\r\n"
                    connectionSocket.send(serverResponse)
                    connectionSocket.close()
                    exit()
                    #print 'Not the correct form'
                else:
                    headerName = currentMessage.split(":")
                    headerNameLower = headerName[0].lower()
                    #print headerNameLower
                    if headerNameLower != 'connection':
                        serverRequest = serverRequest + currentMessage
        # Request to be sent to the server
        serverRequest = serverRequest + "Connection: close\r\n\r\n"
        #print serverRequest

        serverSocket = socket(AF_INET, SOCK_STREAM)
        # you have to change the port number later
        #print urlParts[1]
        #print urlRequest
        #print urlPort
        serverSocket.connect((urlRequest, urlPort))
        serverSocket.send(serverRequest)
        serverResponse = serverSocket.recv(10000)
        serverCurrent = serverResponse
        while len(serverCurrent) > 0:
            serverCurrent = serverSocket.recv(10000)
            serverResponse = serverResponse + serverCurrent
        # send the serverResponse to the client and then close the connection
        connectionSocket.send(serverResponse)
    elif requestSplits[0] == 'POST' or requestSplits[0] == 'PUT' or requestSplits[0]== 'HEAD':
        #print "This has not been implemented"
        serverResponse = "HTTP/1.0 501 Not Implemented\r\n"
        connectionSocket.send(serverResponse)
    connectionSocket.close()
