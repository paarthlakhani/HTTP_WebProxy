#!/usr/bin/python
# Author: Paarth Lakhani
# uid: u0936913

"""
Final version of HTTP Web Proxy:
Requirements as mentioned in the assignment are completed.
"""
from socket import *
import sys 
from urlparse import urlparse 
import re
import multiprocessing as mp
import hashlib

"""
Function connects to the host server and sends a request that has
been received from the client.
After receiving it, it checks whether the response is malware file or no.
It then sends the appropriate response to the client.
"""
def proxy_server(serverRequest, host, urlPort):
    try:
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.connect((host, urlPort))
        serverSocket.send(serverRequest)
        serverResponse = serverSocket.recv(10000)
        serverCurrent = serverResponse
        while len(serverCurrent) > 0: 
            serverCurrent = serverSocket.recv(10000)
            serverResponse = serverResponse + serverCurrent
        serverSocket.close()
        # headers of the response
        content = re.split("\\r\\n\\r\\n", serverResponse,1)[0]
        # content body of the response
        first_line = re.split("\\r\\n\\r\\n", serverResponse,1)[1]
        # checks whether the body is malware or no.
        malware_present = is_malware(first_line)
        if malware_present is True:
            # It is a malware. Send appropriate response
            first_line = "<html>\n"
            first_line += " <head><h2>Contains Malware</h2></head>\n"
            first_line += "   <body>\n"
            first_line += "    This request contains malware.!\n"
            first_line += "   </body>\n"
            first_line += "</html>\n"
            
            new_content = ""
            # changing the headers in response.
            headers = content.splitlines()
            for i in range(len(headers)):
                headerName = headers[i].split(":")
                headerNameLower = headerName[0].lower()
                if headerNameLower == 'content-type':
                    new_content = new_content + "Content-type: text/html\n"
                elif headerNameLower == 'content-length':
                    new_content = new_content + "Content-Length: "+str(len(first_line))+"\n"
                else:
                    new_content = new_content + headers[i] + "\n"
            return (new_content+"\r\n\r\n"+first_line)
        return (content+"\r\n\r\n"+first_line)
    except Exception as e:
        print 'Caught Exception',type(e)
        raise
    finally:
        serverSocket.close()

"""
Function that checks that the headers that are sent by the client are in the
correct format of: <header_name> : <header_value>. We do not include connection header in this function. connection header is added later in the function where this function was called.

return headers as is, if the headers are in the correct format; else, return None.
"""
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

"""
Main function that is called by the new incoming socket.
This function receives request from the client, it parses the request and 
forms a request that should be sent to the host server to get a response back.

Browsers send a blank line and then they a request.
Telnet sends a request directly.
"""
def new_client(connectionSocket):
    try:
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
                try:
                    if httpVersion != "HTTP/1.0":
                        raise TypeError("HTTP/1.0 not implemented")
                except TypeError as e:
                    raise TypeError("HTTP/1.0 not implemented")
                urlComponents = urlparse(requestComponents[1])
                urlPort = urlComponents.port
                host = urlComponents.netloc
                path = urlComponents.path
                if urlPort is None:
                    # default port
                    urlPort = 80
                else:
                    # change the host name
                    m = re.search(":",urlComponents.netloc)
                    host = urlComponents.netloc[:m.start()]
                requestLine = ""
                requestLine += methodType + " " + path + " " + httpVersion + "\r\n"
                requestLine += "Host: " + host + "\r\n"
                # If the headers are in the correct format, requestLine is the requestLine containing all the headers, else requestLine is None. 
                #
                requestLine = check_header_format(headers, requestLine)
                if requestLine is None:
                    serverResponse = "HTTP/1.0 400 Bad Request\r\n"
                else:
                    requestLine += "Connection: close\r\n\r\n"
                    try:
                        serverResponse = proxy_server(requestLine, host, urlPort)
                    except Exception as e:
                        raise
                connectionSocket.send(serverResponse)
            else:
                serverResponse = "HTTP/1.0 501 Not Implemented\r\n"
                connectionSocket.send(serverResponse)
    except Exception as e:
        serverResponse = ('Caught Exception' + str(type(e)))
        connectionSocket.send(serverResponse)
        #print 'Caught Exception',type(e)
        raise
    finally:
        connectionSocket.shutdown(SHUT_RDWR)
        connectionSocket.close()

"""
Function to check whether the response returned by the host server is malware
or no.
Argument: content body of response which might be the malware.
Returns true if the response is a malware; else, it return true.
"""
def is_malware(argument): 
    try:
        m = hashlib.md5()
        m.update(argument)
        hash = m.hexdigest() # md5sum

        cymru_socket = socket(AF_INET, SOCK_STREAM)
        ip = gethostbyname('hash.cymru.com')
        port = 43
        cymru_socket.connect((ip,port))
        request = 'begin\r\n'+hash+'\r\nend\r\n'
        cymru_socket.send(request)
        cymru_response = cymru_socket.recv(10000)
        response_line = cymru_response.splitlines()[2]
        isResponse = response_line.split()[2] # number or "No DATA"
        try:
            responseCode = int(isResponse) # Malware
            return True
        except ValueError:
            return False # not Malware
    except Exception as e:
        print 'Caught exception',type(e)
        raise
    finally:
        cymru_socket.shutdown(SHUT_RDWR)
        cymru_socket.close()
"""
Main method. Method where the socket is open to accept connections concurrently.
Each accepted socket connection is added into the process array and the socket
starts listening on a different thread.
"""
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
        try:
            p = mp.Process(target=new_client, args=(connectionSocket,))
            processes.append(p)
            p.start()
        except Exception as e:
            pass