import socket
from carserver import ServerCar

import time
import sys
from image_transform import ImgTransform
import cv2
import torch

HOST = ""  # Standard loopback interface address (localhost)
PORT = 7777  # Port to listen on (non-privileged ports are > 1023)


def server():
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
                    if command:
                        command[0] = command[0].upper()

                    match command:
                        case ["M", *params]:
                            car.move(*[int(x) for x in params])
                        case ["C", *params]:
                            car.servo(*[int(x) for x in params])
                        case ["T", *params]:
                            car.move(*[int(x) for x in params][:-1])
                            time.sleep(float(params[-1]))
                            car.stop()
                        case _:
                            car.stop()
                except TypeError as e:
                    print(e)


def locate():
    videoFeed = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    print("Opened video feed")
    ret, frame = videoFeed.read()
    space_finder = ImgTransform(frame)

    model = torch.hub.load("ultralytics/yolov5", "custom", path="yolonetwork.pt")

    i = 0
    while videoFeed.isOpened():
        videoFeed.set(cv2.CAP_PROP_POS_MSEC, (i * 66))
        ret, frame = videoFeed.read()

        frame = space_finder.transform(frame)

        # cv2.imshow("Demo", frame)
        # cv2.waitKey(1)

        if ret == False:
            break

        results = model(frame)
        output = results.render()
        cv2.imshow("Demo", output[0])
        cv2.waitKey(1)

        i += 1

    videoFeed.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print("Staring location function")
    locate()
    print("start server?")
    input()
    server()
