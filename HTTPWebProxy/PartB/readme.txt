Author: Paarth Lakhani
uid: u0936913
Assignment PA1_b

In this assignment, I can succesfully handle multiple requests concurrently. I have tested the proxy
as mentioned in the Concurrency test and More sophisticated test paragraphs mentioned in the 
section 2.1.1.
All other functionality remains the same. 

Start the proxy server:
Go to the directory where WebProxy3.py is placed. Then do the command:
    python WebProxy3.py <port number>. I considered the port number: 2112.

Configure the browser to use my proxy server:
Use Firefox 15 and make the changes as mentioned in the assignment so that the browser uses
my proxy. I am not able to load HTTPS web pages and TA told me that we are not required to load
HTTPS webpages

Few Links that pass my proxy: (others also should also pass without HTTPS)

http://www.cs.utah.edu/~kobus/simple.html
http://www.cs.utah.edu/
http://www.geeksforgeeks.org/

It works through telnet as well. In the first part, I had an arrangement made for telnet
such that we could enter multiple headers (multiple lines). The request would be sent to the proxy server only when
we press 'enter' twice in the command prompt. But as I was checking in the browser, it doesn't work
because browser doesn't send a blank line at the end of the request. Unfortunately, I had to remove
the multiple line feature. So, in order to enter multiple lines in the telnet, we should write
the request in a text editor like: 

POST http://www.cs.utah.edu/~kobus/simple.html HTTP/1.0
Host: www.cs.utah.edu
Content-Type: text/html
Connection: open

Start telnet as: 
telnet 127.0.0.1 2112 (assuming the server is runnning on port 2112)

Then copy and paste the entire request above along with the new line. My proxy would then handle
the request appropriately.
The proxy does handle multiple lines. It is just that I am not able to enter multiple lines in
telnet. Telnet takes the first 'enter' as the end of the request and sends it off.