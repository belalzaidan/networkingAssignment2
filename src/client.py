'''
Imorting the necessary dependicies. This includes argparser module,
socket module, sys module and one additional module (http.client)
which helps us recognize the error type based on the provided
status code.
'''
from argparse import *
from socket import *
from http.client import responses
import sys

def main():
    '''
    In the main function, we first set up the argument parser,
    define the host and port numbers if not provided by the client
    and we send the request to the server.
    '''
    # We start with setting up argument parser
    parser = ArgumentParser(description='')
    parser.add_argument('-i', '--host', help='Host IP')
    parser.add_argument('-p', '--port', type=int, help='Port')
    parser.add_argument('-f', '--file', type=str, help='Path to the input file') # file argument
    args = parser.parse_args()

    # Setting default values for host and port if not provided.
    # If provided, then they are to be validated.
    if args.host:
        if validate_ip(args.host):
            host_ip = args.host 
        else: 
            print("\nYour ip address must be in this format: x.x.x.x\n"+
                  "Only numbers and not higher than 255\n")
            sys.exit()
    else: host_ip = '127.0.0.1'
    
    if args.port:
        if  validate_port(args.port):
            port = args.port
        else: 
            print("\nYour port must be within the range [1024,65553]\n")
            sys.exit()
    else: port = 22000

    # We create a new socket and call it clientSocket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    # We then connect it to the server host and port
    clientSocket.connect((host_ip, port))
    print(f"\nClient is connected to ip: {host_ip} and port: {port}")
    
    # The desired file coming from the arguments and located in
    # args.file will be parsed and we will define it in a String
    # object called httpRequest 
    httpRequest = f"GET /{args.file} HTTP/1.1\r"

    # Sending the HTTP request 
    clientSocket.sendall(httpRequest.encode())
    # Recieving a response
    response = clientSocket.recv(1024).decode()
    # From the response, we get the status code
    status_code = int(response.split(" ")[1])

    # The message to the client will be depending on the status code
    # that we defined erlier
    if status_code == 200:
        print(f"File was successfully found!\nStatus Code: {status_code} {responses[status_code]}\n")
    else:
        print(f"An Error occured!\nStatus Code: {status_code} {responses[status_code]}\n")
        
    # This loop holds the client on so it doesn't disconnect
    # unexpectedly
    while True:
        user_input = input("Press 'q' to quit: ")
        if user_input.lower() == 'q':
            break


def validate_ip(ip):
    '''
        This function takes in an IP and returns a boolean
        wheather the IP is valid or not
    '''
    parts = ip.split('.')
    if len(parts) != 4: return False
    for part in parts:
        try:
            if not 0 <= int(part) <= 255 : return False
        except ValueError:
            return False
    return True

def validate_port(port):
    '''
        This function takes in an integer, and returns a boolean
        wheather it's valid as a port number or not
    '''
    try: return 1024 <= port <= 65553 
    except:
        print("An error has occurd while validation")
        return False

main()
