from enum import Enum
from smbus2 import SMBus
from carserver import DIRECTION, CMD
import math


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


class ClientCar:

    """
    Interface for sending / recieving commands to the car
    """

    def __init__(self):
        self.car = YBCar()

    def recieve_command(self, data: bytearray):
        """
        Parses a given data packet and forwards the command to the robot

        Args:
            data (bytearray[8]): 8 bytes structured in this format

            [cmd][arg][arg][arg]...
        """

        cmd = data.pop(0)
        print(cmd)
        if cmd == CMD.MOVE:
            print("moving...")
            self.car.ctrl(*data[:4])
        if cmd == CMD.STOP:
            print("stopping...")
            self.car.stop()
        if cmd == CMD.SERVO:
            print("starting...")
            self.car.servo(*data[:2])