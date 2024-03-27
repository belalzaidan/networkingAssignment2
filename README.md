
# DATA2410 - Oblig 2 &nbsp;&nbsp; <a href="https://github.com/belalzaidan"><img src="https://cdn4.iconfinder.com/data/icons/iconsimple-logotypes/512/github-512.png" style="max-width:20px; filter: invert(60%)"></img></a>


### Achieved goals behind this assignment.


**Task 1: Making a Simple Web Server:**

- Developed a foundational web server capable of processing one request at a time.
- Implemented essential features like request parsing, file retrieval, and response generation.

**Task 2: Crafting an HTTP Client:**

- Created a user-friendly HTTP client using Python's argparse module for command-line interactions.
- Enhanced client-server communication by enabling customized server connections and error handling.

**Task 3: Introducing Multi-Threading to the Server:**

- Improved server efficiency by integrating multi-threading for handling multiple client requests simultaneously.


$~$
#### \#  **Task 1 - Making a simple webserver (server.py)**

In this task, we had to create a basic web server that can handle one HTTP request at a time. The server should accept and parse the HTTP request, retrieve the requested file from its file system, construct an HTTP response message with header lines, and send the response directly to the client. If the requested file was not found, the server should return an HTTP "404 Not Found" message.

To Acheive that, we placed an HTML file (index.html) in the same directory as the server code. 
We start the server either through the terminal or directly within *VSC*. As a client, we access the server's files using a web browser. To do this, we enter the server's IP address and port in the browser's address bar, followed by the desired file name.


 When providing this address, which include the requested IP, port and file:
 `http://127.0.0.1:22000/index.html`

 This HTML page would be the server's response: 

<img src="task-1~200 OK.png"></img>
<small>Original design by: <a href="https://codepen.io/ambercheydesigns">Amber Martineau</a></small>

$~$

If the requested file does not file does not exsist, the client gets this response:

<img src="task-1~404 Not Found.png"></img>

After a client is connected, the server terminal logs the received request along with the corresponding status code that the client has received, as illustrated below:

```c
The server is ready to receive
Connected to: ('127.0.0.1', 64468) // client address
Received request: GET /index.html HTTP/1.1
Host: 127.0.0.1:22000
Connection: keep-alive

... (other details) ...

Server responded with: 200 OK
```
$~$
#### \# **Task 2 - Making a web client (client.py)**

In this task, we've taken our project a step further by creating an HTTP client. This client lets us communicate with our server directly using Python's ```argparse``` module, without needing to use a web browser.

Example on how you can run the client:

```c
python3 client.py -i '127.0.0.1' -p 22000 -f index.html
```

In this case, we get a positive response that the file exists, along with a status code:
```c
Client is connected to ip: 127.0.0.1 and port: 22000
File was successfully found!
Status Code: 200 OK
```
The server terminal also gives us a summary of the request and the response:
```c
The server is ready to receive // Indicates that the server is listenning 
Connected to: ('127.0.0.1', 56131)
Received request: GET /index.html HTTP/1.1
Server responded with: 200 OK
```
We also had to handle a case where a client may request a file that doesn't exist. Example:
```c
python3 client.py -i '127.0.0.1' -p 22000 -f home.html
```
And the response is as following:

**✶ Client side:**
```c
Client is connected to ip: 127.0.0.1 and port: 22000
An Error occured!
Status Code: 404 Not Found
```
**✶ Server side:**
```c
Connected to: ('127.0.0.1', 56892)
Received request: GET /home.html HTTP/1.1
Server responded with: 404 Not Found
```
Something to note is that currently, our HTTP server is configured to manage each HTTP request one by one. Let's say an HTTP request takes in average 800ms to be handled, this means that 3 requests recieved at the same time will be queued, and all together shall have gotten their response after 2400ms. 

$~$
#### \# **3 - Task 3: Making a multi-threaded web server (multithreadServer.py)**

In this part, we've leveled up our web server by adding multi-threading capability. Now, when a client connects to our server, it doesn't have to wait for other clients' requests to finish processing. Each client gets its own thread, allowing multiple clients to be served at the same time. This improvement makes our server more efficient and responsive.

While the server is running, clients can connect using the same terminal command:
`python3 client.py -i '127.0.0.1' -p 23000 -f index.html`. The difference lies in our ability to run multiple clients simultaneously. Here's how it appeared in the server terminal:
```c
The server is ready to receive

Server connected by  ('127.0.0.1', 62863)
Received request: GET /index.html HTTP/1.1
Server responded with: 200 OK

Server connected by  ('127.0.0.1', 62888)
Received request: GET /home.html HTTP/1.1
Server responded with: 404 Not Found
```
Unlike in the previous task, clients now only disconnect if they choose to by entering 'q' in their terminal:
```c
python3 client.py -p 23000 -f index.html

Client is connected to ip: 127.0.0.1 and port: 23000
File was successfully found!
Status Code: 200 OK

Press 'q' to quit: █
```
Upon disconnection, an indication appears in the server terminal, specifying which client with which address disconnected:
```c
Client disconnected: ('127.0.0.1', 62888)
Client disconnected: ('127.0.0.1', 62863)
```
In summary, adding multi-threading to our web server has made a big difference as we saw. The server in this case can handle lots of clients at once by setting up the TCP connection through another port, and therefore providing service to the client request in a separate thread. This means quicker responses for everyone using the server.
$~$
