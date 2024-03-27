'''
Imorting the necessary dependicies. This includes argparser module,
socket module, sys module and one additional module (http.client)
which helps us recognize the error type based on the provided
status code.
'''
from socket import *
import _thread as thread
import sys
from http.client import responses


def handleClient(connection, address):
    """
    A function to handle a client. It takes the ready connection 
    from the main function and completes it. It has two inputs:
    - connection: This holds the connection socket.
    - address: This holds the client's address. We use it to
    recognize which client has connected or disconnected.
    We do exactly what we do in the normal server when it comes 
    to client handling.
    """
    while True:
        try:
            request = connection.recv(1024).decode()
            if not request:
                break
            print("Received request:", request)
        

            headers = request.split('\n')
            filename = headers[0].split()[1]

            try:
                with open('resources' + filename, 'r') as file:
                    html_content = file.read()
                response = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + html_content
            except FileNotFoundError:
                with open('resources/404NotFound.html', 'r') as file:
                    html_content = file.read()
                response = "HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n" + html_content

            status_code = int(response.split(" ")[1])
            print(f"Server responded with: {status_code} {responses[status_code]}\n")
            
            connection.sendall(response.encode())
        # When a client disconnects, this will lead to an exception.
        # We handle this exception, and we print the clients address.
        except ConnectionResetError:
            print(f"Client disconnected: {address}")
            break

    connection.close()


def main():
    """
    In the main function and as usual, we create a server socket,
    listen for new connections and spawn a new thread whenever a 
    new connection joins the socket.
    """
    # Creating, binding and listenning..
    serverPort = 23000
    serverSocket = socket(AF_INET, SOCK_STREAM)
    try:
        serverSocket.bind(('', serverPort))

    except:
        print("Bind failed. Error : ")
        sys.exit()
    serverSocket.listen()
    print(f'The server is ready to receive on (127.0.0.1, {serverPort})')
    # Once a client is connect, we accept their request.
    # We spawn a thread and we handle the request using 
    # handleClient() function.
    while True:
        conn, addr = serverSocket.accept()
        print('\nServer connected by ', addr)
        thread.start_new_thread(handleClient, (conn,addr))

    serverSocket.close()


if __name__ == '__main__':
    main()
