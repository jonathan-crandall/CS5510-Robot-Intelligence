from enum import Enum
from smbus2 import SMBus
from carserver import CMD, DIRECTION, Command
import pickle
import math
import time
import RPi.GPIO as GPIO
import threading

# this class was shamelessly stoen straing from yahboom
# which is fine because its hot garabe and had to be modified 
# in order to support better commands
class YBCar(object):
    def get_i2c_device(self, address, i2c_bus):
        self._addr = address
        if i2c_bus is None:
            return SMBus(1)
        else:
            return SMBus(i2c_bus)

    def __init__(self):
        # Create I2C device.

        self._device = self.get_i2c_device(0x16, 1)

    def write_u8(self, reg, data):
        try:
            self._device.write_byte_data(self._addr, reg, data)
        except:
            print("write_u8 I2C error")

    def write_reg(self, reg):
        try:
            self._device.write_byte(self._addr, reg)
        except:
            print("write_u8 I2C error")

    def write_array(self, reg, data):
        try:
            # self._device.write_block_data(self._addr, reg, data)
            self._device.write_i2c_block_data(self._addr, reg, data)
        except:
            print("write_array I2C error")

    def ctrl(self, l_dir: DIRECTION, l_speed: int, r_dir: DIRECTION, r_speed: int):
        try:
            reg = 0x01
            data = [l_dir, l_speed, r_dir, r_speed]
            self.write_array(reg, data)
        except:
            print("Ctrl_Car I2C error")

    def Control_Car(self, speed1, speed2):
        try:
            if speed1 < 0:
                dir1 = 0
            else:
                dir1 = 1
            if speed2 < 0:
                dir2 = 0
            else:
                dir2 = 1

            self.Ctrl_Car(dir1, int(math.fabs(speed1)), dir2, int(math.fabs(speed2)))
        except:
            print("Ctrl_Car I2C error")

    def Car_Run(self, speed1, speed2):
        try:
            self.Ctrl_Car(1, speed1, 1, speed2)
        except:
            print("Car_Run I2C error")

    def stop(self):
        try:
            reg = 0x02
            self.write_u8(reg, 0x00)
        except:
            print("Car_Stop I2C error")

    def Car_Back(self, speed1, speed2):
        try:
            self.Ctrl_Car(0, speed1, 0, speed2)
        except:
            print("Car_Back I2C error")

    def Car_Left(self, speed1, speed2):
        try:
            self.Ctrl_Car(0, speed1, 1, speed2)
        except:
            print("Car_Spin_Left I2C error")

    def Car_Right(self, speed1, speed2):
        try:
            self.Ctrl_Car(1, speed1, 0, speed2)
        except:
            print("Car_Spin_Left I2C error")

    def Car_Spin_Left(self, speed1, speed2):
        try:
            self.Ctrl_Car(0, speed1, 1, speed2)
        except:
            print("Car_Spin_Left I2C error")

    def Car_Spin_Right(self, speed1, speed2):
        try:
            self.Ctrl_Car(1, speed1, 0, speed2)
        except:
            print("Car_Spin_Right I2C error")

    def servo(self, id, angle):
        print(f"moving servo here with {id}, {angle}")
        try:
            reg = 0x03
            data = [id, angle]
            if angle < 0:
                angle = 0
            elif angle > 180:
                angle = 180
            self.write_array(reg, data)
        except:
            print("Ctrl_Servo I2C error")


class CarClient:

    """
    Interface for sending / recieving commands to the car
    """

    def __init__(self, debug: bool):
        self.car = YBCar()
        self.debug = debug

    def recieve_command(self, data: bytearray):
        """
        Parses a given data packet and forwards the command to the robot

        Args:
            data (bytearray[8]): 8 bytes structured in this format

            [cmd][arg][arg][arg]...
        """
        cmd: Command = pickle.loads(data)
        if cmd.type == CMD.MOVE:
            print("moving...")
            self.car.ctrl(*cmd.params)
        elif cmd.type == CMD.STOP:
            print("stopping...")
            self.car.stop()
        elif cmd.type == CMD.SERVO:
            print("Moving Servo...")
            self.car.servo(*cmd.params)
        else:
            print(f"Invalid argument {cmd.type}")


class CollisionDetector(threading.Thread):
    """
    Runs the internal collussion detection models, so that the control
    server doesn't have to worry about it

    """
    def __init__(self, car: CarClient, *args, **kwargs) -> None:
        """

        Args:
            car (CarClient): The yahboom low IC2 car model
        """
        super().__init__(*args, **kwargs)
        self.car = car

    def run(self):
        
        # Init the front facing reflection sencors
        TL1 = 13
        TL2 = 15
        TR1 = 11
        TR2 = 7

        GPIO.setmode(GPIO.BOARD)

        GPIO.setwarnings(False)

        GPIO.setup(TL1, GPIO.IN)
        GPIO.setup(TL2, GPIO.IN)
        GPIO.setup(TR1, GPIO.IN)
        GPIO.setup(TR2, GPIO.IN)

        value_store = []
        while True:

            value_store.append(
                (
                    not GPIO.input(TL1),
                    not GPIO.input(TL2),
                    not GPIO.input(TR1),
                    not GPIO.input(TR2),
                )
            )

            # If reflection not detected, like on tape
            if all([any(x) for x in value_store]):
                print("Table edge detected")
                self.car.car.stop()
                
            # Store a history to make sure that we don't get some incorrect reads
            if len(value_store) > 5:
                value_store.pop(0)

            if self.car.debug:
                print(f"{value_store}")
            time.sleep(0.01)
