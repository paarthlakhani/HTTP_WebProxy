Author: Paarth Lakhani
uid: u0936913
Assignment PA1_Final

Completed the first programming assignment.
All the requirements and goals have been completed. much similar to the previous submissions. The assignment report has been submitted through canvas.

Configure the browser to use my proxy server:
Use Firefox 15 and make the changes as mentioned in the assignment so that the browser uses my proxy. 

The final version of the web proxy identifies malware by querying the cymru website. Thus, this web proxy identifies all the malware that are identified as malware by cymru.

If the malware file has been returned from the server, the proxy creates a HTML page indicating that the file returned is malware. The proxy server sends the original response back if the file requested is not malware.

I downloaded 7 - 8 educational malwares from the website. All but one were correctly identified as malware. Maybe cymru doesn't recoginize that malware as malware. Three other HTML files were requested through the HTTPWebProxy

I tested the code the way it is mentioned in the section 2.1.1. All the files are hosted the HTTP Web Proxy and can be requested through the telnet client or firefox.

Start my server:
1. Go to the folder where WebProxy3.py is submitted and use the command:
    python WebProxy3.py <port number>;
    <port number> can be anything between 2112 adn 2120 as mentioned by the professor.
    I usually use 2112, 2113, or 2114.

Go the folder where the good and malware files are placed and do the command to start SimpleHTTPServer:
python -m SimpleHTTPServer 8000 
and files could be requested by the client as it is done by any other client to get anything in the folder that hosts the SimpleHTTPServer.

Few of the requests are:
GET http://0.0.0.0:8000/malware1.file HTTP/1.0
GET http://0.0.0.0:8000/malware2.file HTTP/1.0
GET http://0.0.0.0:8000/malware3.file HTTP/1.0
( 0.0.0.0 is IP of HTTPWebProxy and 8000 is the port)

Other requests are:
GET http://www.cs.utah.edu/~kobus/simple.html HTTP/1.0
GET http://www.cs.utah.edu/ HTTP/1.0
GET http://www.geeksforgeeks.org/ HTTP/1.0