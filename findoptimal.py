import time
from typing import List

from pipython import GCSDevice
from pipython.interfaces.gcsdll import get_dll_name

from pathlib import Path

#from motorcontrolbackend import M406Motor
import random

DLL_PATH = "PI_GCS2_DLL.dll"

with GCSDevice() as pidevice:
    deviceX = pidevice.EnumerateTCPIPDevices()
    print(deviceX)
deviceY = GCSDevice.EnumerateUSB(mask='')
#grid with a size
min = [0,0]
max = [10,10]

async def find_optimal():
    max_output = 0
    max_place = [0,0]
    deviceY.position(min[0])
    deviceX.position(min[0])
    await (not deviceX.is_moving() and not deviceY.is_moving())
    for i in range(max[1]):
        deviceY.position(i)
        await (not deviceY.is_moving())
        while (deviceX.position()<max[0]):
            deviceX.forward(1)
            await (not deviceX.is_moving())
            output = random.randint(1,10) #opm read output
            if output > max_output:
                max_output = output
                max_place = [deviceX.position(),deviceY.position()]
    return max_output, max_place

max_output, max_place = find_optimal()
