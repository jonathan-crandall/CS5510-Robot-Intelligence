from enum import Enum
from dataclasses import dataclass
from typing import Optional
import pickle
from socket import socket
from dataclasses import dataclass


@dataclass
class DIRECTION:
    FWD = 1
    REV = 0


class CMD(Enum):
    MOVE = 1
    SERVO = 2
    STOP = 3


@dataclass
class Command:
    type: CMD
    params: list = None


class ServerCar:
    def __init__(self, conn: socket) -> None:
        self.connection: socket = conn

    def send(self, command: Command):
        binary = pickle.dumps(command)
        self.connection.sendall(binary)

    def move(self, left_velocity, right_velocity):
        left_direction = DIRECTION.FWD
        right_direction = DIRECTION.FWD

        if left_velocity < 0:
            left_velocity = abs(left_velocity)
            left_direction = DIRECTION.REV

        if right_velocity < 0:
            right_velocity = abs(right_velocity)
            right_direction = DIRECTION.REV

        self.send(
            Command(
                CMD.MOVE,
                [left_direction, left_velocity, right_direction, right_velocity],
            )
        )

    def stop(self):
        self.send(Command(CMD.STOP))

    def servo(self, id, angle):
        self.send(Command(CMD.SERVO, [id, angle]))
