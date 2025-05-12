# tcp_server.py
import socket
from config import PORT

def create_server_socket(ip, port=PORT):
    """
    The function `create_server_socket` creates a TCP server socket bound to a specified IP address and
    port.
    
    :param ip: IP address on which the server socket will listen for incoming connections
    :param port: Port number that the server socket will bind to. 
    :return: socket object that represents a TCP server socket bound to the specified IP address and port number.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    s.listen(1)
    print(f"TCP server listening at {ip}:{port}")
    return s
