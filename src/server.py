from socket import *
from http.client import responses # Using this library, we get the status code by providing the error number

"""
We start by creating a socket, and binding the it to a host IP
and a port
"""
# Create a socket called "serverSocket"
serverSocket = socket (AF_INET, SOCK_STREAM)
# Define server's host IP and port
port = 22000
server_ip = '127.0.0.1'

# Binding socket to host and port
serverSocket.bind((server_ip, port))

# Listening for incoming connections
serverSocket.listen(1)
print(f'The server is ready to receive on ({server_ip}, {port})')

# Server waits on accept() for connections
while True:
    conn, addr = serverSocket.accept()
    print("Connected to:", addr)

    # Define the recieved request
    request = conn.recv(1024).decode()
    print("Received request:", request)

    # Analayzing the request elements to extract the requested filename
    headers = request.split('\n')
    filename = headers[0].split()[1]

    '''
    Here we start checking if the requested file exist. If so,
    it shall return a 200 OK status code, and eventually the content
    of that file
    '''
    try:
        with open('resources' + filename, 'r') as file:
            html_content = file.read()
        response = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + html_content
    except FileNotFoundError:
        with open('resources/404NotFound.html', 'r') as file:
            html_content = file.read()
        response = "HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n" + html_content
        
    # Status code depending on the server response (OK/Not Found)
    status_code = int(response.split(" ")[1])
    print(f"Server responded with: {status_code} {responses[status_code]}\n")
    
    # Sending the response to the client, and closing the connnection
    conn.sendall(response.encode())
    conn.close()
