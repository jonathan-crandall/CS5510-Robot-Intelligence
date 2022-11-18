# echo-client.py

import socket
from carmodel import ClientCar


SERVER_HOST = "144.39.208.62"  # The server's hostname or IP address
# SERVER_HOST = "127.0.0.1"
PORT = 7777  # The port used by the server

# Create connection with car
car = ClientCar()


print("Running client...")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((SERVER_HOST, PORT))

    while True:
        data: bytes = bytearray(s.recv(32))
        print(data, type(data))
        if not data:
            break
        car.recieve_command(data)


print(f"Exit!")
