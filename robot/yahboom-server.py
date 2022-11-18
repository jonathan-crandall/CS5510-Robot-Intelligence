import socket
from carserver import ServerCar
import time

HOST = ""  # Standard loopback interface address (localhost)
PORT = 7777  # Port to listen on (non-privileged ports are > 1023)

car = ServerCar()

print("Running server...")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        data = car.move(80, -80)
        print(data)
        conn.sendall(data)
        time.sleep(5)
        data = car.stop()
        print(data)
        conn.sendall(car.stop())
