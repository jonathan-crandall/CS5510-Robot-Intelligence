import socket
from carserver import ServerCar

import time

HOST = ""  # Standard loopback interface address (localhost)
PORT = 7777  # Port to listen on (non-privileged ports are > 1023)


print("Waiting for client connection...", end="\r")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    print(f"Connected at {addr}      ")
    with conn:
        car = ServerCar(conn)
        while True:
            try:
                print("Commands: {M, C, S} {params...}")
                command = input().split()
                command[0] = command[0].upper()
                match command:
                    case ["M", *params]:
                        car.move(*[int(x) for x in params])
                    case ["C", *params]:
                        car.servo(*[int(x) for x in params])
                    case _:
                        car.stop()
            except TypeError as e:
                print(e)
