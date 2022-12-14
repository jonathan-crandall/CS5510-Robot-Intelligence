import socket
from threading import Thread
from queue import Queue
import time
import sys
import cv2
import torch
import pandas as pd

# Local packages found in ./robot
from carserver import ServerCar
from image_transform import ImgTransform
from locationtracking import LocationTracker
from camera_read import image_server, process as rpi_process
HOST = ""  # Standard loopback interface address (localhost)
PORT = 7777  # Port to listen on (non-privileged ports are > 1023)


def server(commandQueue: Queue):
    """
    This is the function that runs the command control server, and manages
    communication with the rasberry pi for movement using small packets
    sent over a socket server

    Args:
        commandQueue (Queue): a shared queue that other threads can put commads into
    """

    # Establish connection
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
                    # Wait to recieve command from other threads
                    command = commandQueue.get(True, None)

                    # Useful for manual input
                    if command:
                        command[0] = command[0].upper()

                    # Parse threads
                    match command:
                        case ["M", *params]:
                            car.move(*[int(x) for x in params])
                        case ["C", *params]:
                            car.servo(*[int(x) for x in params])
                        case ["T", *params]:
                            print(params)
                            car.move(*[int(x) for x in params][:-1])
                            time.sleep(float(params[-1]))
                            car.stop()
                        case ["Q", *params]:
                            break
                        case ["S"]:
                            car.stop()
                        case _:
                            print(f"Unknown command {command}")
                            car.stop()

                except TypeError as e:
                    print(e)


def locate(commandQueue: Queue):
    """
    Runs the image recognition algorithm for locating the robot and ball with
    the overhead camera.

    Args:
        commandQueue (Queue): Shared command queue to send commands to
    """

    # Establish video feed, calculate initial translation

    videoFeed = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    print("Opened video feed")
    ret, frame = videoFeed.read()
    space_finder = ImgTransform(frame)

    # Build the tracker model using the new image bounds
    x_bound, y_bound, *_ = frame.shape
    print("Image Size: ", x_bound, y_bound)
    tracker = LocationTracker(x_bound, y_bound)

    # Init torch image recognition model
    model = torch.hub.load("ultralytics/yolov5", "custom", path="yolonetwork.pt")

    # Tracker varables for the previous locations and frames between
    # ball and robot detection in case of failure
    frame_counter = 0
    pb_loc = None
    pr_loc = None
    ball_not_found = 0

    while videoFeed.isOpened():
        #  Read frame
        videoFeed.set(cv2.CAP_PROP_POS_MSEC, (frame_counter * 66))
        ret, frame = videoFeed.read()

        if ret == False:
            break

        # Transform Frame
        frame = space_finder.transform(frame)

        # Process frame with YOLO
        results = model(frame)
        output = results.render()[0]
        data: pd.DataFrame = results.pandas().xyxy[0]

        frame_counter += 1

        try:
            b_loc = (
                data["xmin"][1],
                data["ymin"][1],
                data["xmax"][1],
                data["ymax"][1],
            )
            r_loc = (
                data["xmin"][0],
                data["ymin"][0],
                data["xmax"][0],
                data["ymax"][0],
            )
        except (KeyError, IndexError):

            # Backup command model to run if not all items are present in object
            # TODO: Add better suicide prevention

            print(f"objects not found {frame_counter}", end="\r")

            # Issue stop command if unable to find ball after N frames
            ball_not_found += 1
            if ball_not_found > 15:
                print(f"havent found ball in {ball_not_found} frames")
                commandQueue.put(["S"])

            # Show output
            cv2.imshow("Demo", output)
            cv2.waitKey(1)
            frame_counter += 1
            continue

        if pb_loc is not None and pr_loc is not None:

            # Derive ball and robot positions, as well as distance needed to travel
            dist, target, ball_center, robo = tracker.track(
                (b_loc, pb_loc), (r_loc, pr_loc)
            )

            # Reset search counter
            ball_not_found = 0

            print(f"Distance to ball{dist}")

            # Annotate and show image with ball path
            cv2.arrowedLine(output, ball_center, target, (255, 0, 255))
            cv2.imshow("Demo", output)
            cv2.waitKey(1)

            # Send command logic
            # Check if ball causes robotic suicide
            if (robo[0] + dist) > (x_bound * 0.9) or (robo[0] + dist < (x_bound * 0.1)):
                print(
                    "\n",
                    (robo[0] + dist),
                    (robo[0] + dist) < (x_bound * 0.1),
                    (robo[0] + dist) > (x_bound * 0.9),
                )
                print("Suicide Prevention!!!")
                commandQueue.put(["S"])
                # Send stop
            # If ball is withtin threshold
            elif abs(dist) < 20:
                # Send stop, you got the ball
                commandQueue.put(["S"])

            elif dist > 80:
                # move at 100
                commandQueue.put(["M", 100, 100])

            elif dist < -80:
                # move at -100
                commandQueue.put(["M", -100, -100])
            elif dist > 0:
                # move at 50
                commandQueue.put(["M", 50, 50])
            elif dist < 0:
                # move at 50
                commandQueue.put(["M", -50, -50])

        elif pb_loc is not None:
            # We add these checks here to send commands even if ball is not present
            if (pb_loc[3] + dist) > (x_bound * 0.9) or (
                pb_loc[1] + dist < (x_bound * 0.1)
            ):
                print("Suicide Prevention w/o ball")
                commandQueue.put(["S"])
                # Send stop

        # Update previous frame postions
        if r_loc is not None:
            pr_loc = r_loc
        pb_loc = b_loc

    videoFeed.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    
    threads = []

    commands = Queue()

    # Each segment allows us to disable certain services for easier debugging, 
    # all are enabled by default

    if "-i" not in sys.argv:
        print("Staring location function ...")
        threads.append(Thread(target=locate, args=[commands],daemon=True))

    if "-s" not in sys.argv:
        print("Starting command and control server ...")
        threads.append(Thread(target=server, args=[commands], daemon=True))
        
    if "-pi" not in sys.argv:
        buffer = Queue()
        print("Starting localized ball tracker ...")
        threads.append(Thread(target=image_server, args=[buffer], daemon=True))
        threads.append(Thread(target=rpi_process, args=[buffer, commands], daemon=True))

    for t in threads:
        t.start()
        
    for t in threads:
        t.join()
