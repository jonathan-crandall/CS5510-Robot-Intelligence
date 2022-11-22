from threading import Thread
import socket
import struct
from carclient import CarClient, CollisionDetector
import cv2
import pickle
import sys

SERVER_HOST = "144.39.208.62"  # The server's hostname or IP address
PORT = 7777  # The port used by the server
CAMERA_PORT = 7778


def videoStream():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, CAMERA_PORT))
    connection = client_socket.makefile("wb")

    cam = cv2.VideoCapture(0)

    img_counter = 0
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    while True:
        ret, frame = cam.read()
        result, frame = cv2.imencode(".jpg", frame, encode_param)
        #    data = zlib.compress(pickle.dumps(frame, 0))
        data = pickle.dumps(frame, 0)
        size = len(data)

        client_socket.sendall(struct.pack(">L", size) + data)
        img_counter += 1


def controller():
    print("Running client...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_HOST, PORT))
        print("Connected!")
        while True:
            data: bytes = bytearray(s.recv(4096))
            print(f"Recieved command size : {len(data)}")
            if not data:
                break
            car.recieve_command(data)


if __name__ == "__main__":
    
    DEBUG = False
    if "-d" in sys.argv:
        DEBUG = True
    # Create connection with car
    car = CarClient(DEBUG)

    # Create camera thread
    print(sys.argv)
    if "-C" in sys.argv:
        print("starting camera app")
        camera_thread = Thread(target=videoStream)
        camera_thread.daemon = True
        camera_thread.start()
    
    # Start thread for collision checking
    collision_thread = CollisionDetector(car, daemon=True)
    collision_thread.start()

    # Start controller listener
    controller()
