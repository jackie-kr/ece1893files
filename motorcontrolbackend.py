import os, sys; sys.path.append(r"C:\Users\jacks\ECE1893\pipython")
import time
from typing import List

from pipython import GCSDevice
from pipython.interfaces.gcsdll import get_dll_name

from pathlib import Path

#from motorcontrolbackend import M406Motor
import random

DLL_PATH = "PI_GCS2_DLL_x64.dll"


class M406Motor(GCSDevice):
    All_M_406_Connected_Devices: List = []

    def __init__(self, device_name: str = "C-863", index=0, dll_path: str = DLL_PATH):
        super().__init__(gcsdll=dll_path)
        self.index = index
        self.device_name = device_name
        self.extreme_value = None
        self.min_position = None
        self.max_position = None
        self.connect()

    def connect(self):
        if len(self.All_M_406_Connected_Devices) == 0:
            pi = GCSDevice(gcsdll=self.dllpath)

            list_of_devices = pi.EnumerateUSB(mask=self.device_name.split(".")[0])
            if len(list_of_devices) == 0:
                raise Exception(f"{self.device_name} is not connected or being used by some other device")

            all_devices: list = pi.OpenUSBDaisyChain(description=list_of_devices[0])
            self.All_M_406_Connected_Devices.extend([
                (i + 1, pi.dcid) for i, v in enumerate(all_devices) if "not connected" not in v
            ])

            if len(self.All_M_406_Connected_Devices) == 0:
                raise Exception(f"No motors found connected to {self.device_name}")

        self.ConnectDaisyChainDevice(*self.All_M_406_Connected_Devices[self.index])
        self.refersence_align()
        self.extreme_value = 0
        self.min_position = int(self.qTMN()['1'])
        self.max_position = int(self.qTMX()['1'])

    def refersence_align(self):
        print(f"Referencing motor: {self}")
        self.SVO({1: True})
        position = self.position()
        speed = self.speed()
        self.speed(1)
        self.FRF()
        while self.is_moving():
            time.sleep(1)
        if position > 0:
            self.position(position)
        while self.is_moving():
            time.sleep(1)
        self.speed(speed)

    def forward(self, val: float):
        self.position(self.position() + val)

    def backward(self, val: float):
        self.position(self.position() - val)

    def position(self, val: float = None):
        if val is None:
            return self.qPOS()["1"]
        else:
            self.MOV({1: val})

    def target_position(self, val: float = None):
        if val is None:
            return self.qMOV()["1"]
        else:
            self.MOV({1: val})

    def speed(self, val: float = None):
        if val is None:
            return self.qVEL()["1"]
        else:
            self.VEL({1: val})

    def stop(self):
        self.position(self.position())

    def extreme(self, val: [-1, 0, 1] = None):
        if val is not None:
            if val == 0:
                self.stop()
                self.extreme_value = val
            elif val == -1:
                self.position(self.min_position)
                self.extreme_value = val
            elif val == 1:
                self.position(self.max_position)
                self.extreme_value = val
        else:
            return self.extreme_value

    def is_moving(self):
        return self.IsMoving()["1"]

    def is_working(self):
        return self.is_moving()


if __name__ == '__main__':
    motor_x = M406Motor(index=0)
    motor_y = M406Motor(index=1)
    print(motor_x.position(), motor_y.position())
    print(motor_x.speed(), motor_y.speed())
    print(motor_x.is_moving())