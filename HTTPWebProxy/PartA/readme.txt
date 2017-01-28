Name: Paarth Lakhani
uid: u0936913

For PA1-A, I have not incorporated for multithreading or multiprocessing. Since, this is not the requirement for part-1, I would be incorporating it in the next part.
Also, for this part, I have used localhost as the hostname. That would be changed for the next part. 

To run my proxy server, please open two command prompts, go to the folder my my program is situated.

On one terminal, do the command:
python WebProxy.py <port>; I have tested the port on port no. 2112; 2113

On other terminal, do the command for starting up the client using telnet:
telnet 127.0.0.1 <port>; the same port that was used to start up the proxy server.

On telnet command, we can issue commands like:
1. GET http://www.cs.utah.edu/~kobus/simple.html HTTP/1.0
2. GET http://www.google.com/ HTTP/1.0

Additional Commands can also be mentioned.

Basic Checking is done:
1. Only GET request is implemented. For all other requests, 501 Not Implemented is issued.
2. Headers have to be in form: header_name: header_value. For others, 400 Bad Request is issued
3. HTTP/1.0 is implemented , for any other HTTP protocol Bad Request is issued.
4. Any Connection header sent to the Proxy server is replaced by Connection: close.

Important Note:
On the client side, when the user enters the request line:
GET http://www.google.com/ HTTP/1.0; and presses "enter", the request is not yet sent. The user can enter additional headers in the command line in the correct format. When the user has completed entering the header names, the user then needs to press "enter" twice to make sure that the request has been finalized and hence, the request line is sent to the host server.

Thank you.!
