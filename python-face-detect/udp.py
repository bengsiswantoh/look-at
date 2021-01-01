import socket
import json

position = {"x": 10, "y": 0}

#byte_message = bytes("Hello, World!", "utf-8")
byte_message = bytes(json.dumps(position), "utf-8")
opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
opened_socket.sendto(byte_message, ("127.0.0.1", 3000))

opened_socket.close()