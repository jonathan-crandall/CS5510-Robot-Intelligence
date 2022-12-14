"""
This file can be run as a standalone rasberry pi monitor, or run in tandem
With the main thread
"""

import socket
import cv2
import pickle
import numpy as np
import struct  ## new
import torch
import queue
import threading
import pandas as pd

HOST = ""
PORT = 7778


def image_server(buffer: queue.Queue):
    """
    Reads a bytestream sent from the yahboom, processes and packages them
    back into an opencv image

    Args:
        buffer (queue.Queue): Queue to store image frames for processing
    """

    # Start listening for server on raspberry pi
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created")
    s.bind((HOST, PORT))
    print("Socket bind complete")
    s.listen(10)
    print("Socket now listening")

    conn, addr = s.accept()

    # Parse packet size coming from the robot
    data = b""
    payload_size = struct.calcsize(">L")
    print("payload_size: {}".format(payload_size))

    while True:

        # Recieve data packets until all are sent
        while len(data) < payload_size:
            data += conn.recv(4096)

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        while len(data) < msg_size:
            data += conn.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        # Load data into a usuable image frame
        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        # Store frame
        buffer.put(frame)


def process(image_buffer: queue.Queue, command_queue: queue.Queue = None):
    """
    Given images from the yahboom camera, processes them to find the location of the ball, and send commands to the sevros to keep the ball in the center of the recticle.

    Args:
        image_buffer (queue.Queue): Image frames
        command_queue (queue.Queue): Command Queue
    """

    # Load torch model
    model = torch.hub.load("ultralytics/yolov5", "custom", path="yolonetwork.pt")

    # Starting angles for picam
    x_angle = 90
    y_angle = 90
        
    # amount moved per check
    CONSTANT = 5
    
    # reset camera position
    command_queue.put(["C", 1, x_angle])
    command_queue.put(["C", 2, y_angle])
            
    while True:
        # thread safety for reading a frame, and clearing the backlog of frames
        # we cant process in time
        frame = image_buffer.get(True)
        with image_buffer.mutex as q:
            image_buffer.queue.clear()

        x_bound, y_bound, *_ = frame.shape

        # Process frame
        results = model(frame)
        output = results.render()[0]
        data: pd.DataFrame = results.pandas().xyxy[0]

        # Grab image position
        try:
            x_min, y_min, x_max, y_max = (
                data["xmin"][0],
                data["ymin"][0],
                data["xmax"][0],
                data["ymax"][0],
            )
        except (IndexError):
            print("PI STREAM: no ball found")
            cv2.imshow("Pi Feed", output)
            cv2.waitKey(1)
            continue

        x_mid, y_mid = (x_max + x_min) // 2, (y_max + y_min) // 2

        # Show annotated frame
        cv2.imshow("Pi Feed", output)
        cv2.waitKey(1)

        # Logic for sending commands
        if command_queue:
            change = False
            if x_mid < x_bound * 0.3:
                # move left
                x_angle += CONSTANT
                change = True
            elif x_mid > x_bound * 0.7:
                # move right
                x_angle -= CONSTANT
                change = True

            if y_mid < y_bound * 0.3:
                # move up
                y_angle -= CONSTANT
                change = True

            elif y_mid > y_bound * 0.5:
                y_angle += CONSTANT
                change = True
                
            if change:
                print(f"{x_mid, y_mid} | {x_max, y_max}")
                command_queue.put(["C", 1, x_angle])
                command_queue.put(["C", 2, y_angle])


if __name__ == "__main__":

    threads = []
    image_buffer = queue.Queue()
    image_stream = threading.Thread(target=image_server, args=[image_buffer])
    image_stream.daemon = True
    threads.append(image_stream)

    image_processor = threading.Thread(target=process, args=[image_buffer])
    image_processor.daemon = True
    threads.append(image_processor)

    for t in threads:
        t.start()

    for t in threads:
        t.join()
