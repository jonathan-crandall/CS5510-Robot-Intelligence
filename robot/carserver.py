from enum import Enum
from dataclasses import dataclass


@dataclass
class DIRECTION:
    FWD = 1
    REV = 0


@dataclass
class CMD:
    MOVE = 0x10
    STOP = 0x20hv
    SERVO = 0x30


class ServerCar:
    def move(self, left_velocity, right_velocity):
        left_direction = DIRECTION.FWD
        right_direction = DIRECTION.FWD

        if left_velocity < 0:
            left_velocity = abs(left_velocity)
            left_direction = DIRECTION.REV

        if right_velocity < 0:
            right_velocity = abs(right_velocity)
            right_direction = DIRECTION.REV

        return bytearray(
            (
                CMD.MOVE,
                left_direction,
                left_velocity,
                right_direction,
                right_velocity,
            )
        )

    def stop(self):
        return CMD.STOP.to_bytes(1, "big")

    def servo(self, id, angle):
        return bytearray((CMD.SERVO, id, angle))
