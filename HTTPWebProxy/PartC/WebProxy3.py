#!/usr/bin/python
# Author: Paarth Lakhani
# uid: u0936913

from socket import *
import sys 
from urlparse import urlparse 
import re
import multiprocessing as mp
import hashlib

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

    isHeaders = re.search("\\r\\n\\r\\n", serverResponse);
    #print isHeaders
    if isHeaders == "None":
        print 'No match'
        content = serverResponse
    else:
        content = re.split("\\r\\n\\r\\n", serverResponse)[1]
    #print content
    #print "Hello Everyone"
    #print serverResponse
    is_malware(content)
   # is_content = re.search("\\r\\n",serverResponse)
   # print is_content.group(1)
    #print serverResponse
    #print is_malware(serverResponse)
    return serverResponse

def check_header_format(headers, requestLine):
    for i in range(len(headers)):
        match = re.search(".:.",headers[i])
        if match is None:
            # It is not in the correct format
            return None
        else:
            headerName = headers[i].split(":")
            headerNameLower = headerName[0].lower()
            if headerNameLower!= 'connection' and headerNameLower!= 'host':
                requestLine += headers[i]+"\r\n"
    return requestLine

# browsers send a blank line and then the request
# from telnet, only the request comes in.\

def new_client(connectionSocket):
    entireRequest = connectionSocket.recv(1024)
    # processing when the request length > 0
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
            requestLine = check_header_format(headers, requestLine)
            if requestLine is None:
                serverResponse = "HTTP/1.0 400 Bad Request\r\n"
            else:
                requestLine += "Connection: close\r\n\r\n"
                serverResponse = proxy_server(requestLine, host, urlPort)
            connectionSocket.send(serverResponse)
        else:
            serverResponse = "HTTP/1.0 501 Not Implemented\r\n"
            connectionSocket.send(serverResponse)
    connectionSocket.shutdown(SHUT_RDWR)
    connectionSocket.close()
    
# argument is the content body of malware.
def is_malware(argument): 
    '''
        Send this to the cymru website.
    '''
    # doing the md5sum hash
    m = hashlib.md5()
    m.update(argument);
    '''
    hash = m.hexdigest();
    #print format(hash,'02x')
    print hash'''
    #print hashlib.md5(argument).hexdigest()
    #m = hashlib.md5(argument.encode())
    #print(m.hexdigest())
    hash = m.hexdigest()
    print hash

    cymru_socket = socket(AF_INET, SOCK_STREAM)
    ip = gethostbyname('hash.cymru.com')
    port = 43
    cymru_socket.connect((ip,port))
    #request = 'begin\r\n'+argument+'\r\nend\r\n'
    request = 'begin\r\n'+hash+'\r\nend\r\n'
    #print request
    #print 'Hello Everyone \n'
    cymru_socket.send(request)
    cymru_response = cymru_socket.recv(10000)
    response_line = cymru_response.splitlines()[2];
    isResponse = response_line.split()[2]
    #print isResponse
    try:
        responseCode = int(isResponse)
        print 'I am a malware'
        #print responseCode
        return True;
    except ValueError:
        print 'I am not a malware'
        return False;
    cymru_socket.shutdown(SHUT_RDWR)
    cymru_socket.close()

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
        # f1db409bf1ff8f356cffb4a5546c34a4 Malware
        # 33ff14f98e8c1d4eed08297e2eaccf51 not Malware
        # p = mp.Process(target=is_malware, args=("f1db409bf1ff8f356cffb4a5546c34a4",))
        processes.append(p)
        p.start()