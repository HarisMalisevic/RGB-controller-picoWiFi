import machine
import sys
import aioble
import bluetooth
import uasyncio as asyncio
from micropython import const


def uid():
    """
    Return the unique ID of the device as a string
    """
    return "{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(
        *machine.unique_id()
    )

MANUFACTURER_ID = const(0x2A29)
MODEL_NUMBER_ID = const(0x2A24)
SERIAL_NUMBER_ID = const(0x2A25)
HARDWARE_REVISION_ID = const(0x2A26)
BLE_VERSION_ID = const(0x2A28)

_GENERIC = bluetooth.UUID(0x180A)

_BLE_APPEARANCE_GENERIC_RGB_CONTROLLER = const(0x1800)

ADV_INTERVAL_MS = 250_000

# Service for Device information 
device_info = aioble.Service(_GENERIC)

# Characteristics for Device information
aioble.Characteristic(device_info, bluetooth.UUID(MANUFACTURER_ID), read=True, initial="HarisovRGB")
aioble.Characteristic(device_info, bluetooth.UUID(MODEL_NUMBER_ID), read=True, initial="0.1")
aioble.Characteristic(device_info, bluetooth.UUID(SERIAL_NUMBER_ID), read=True, initial=uid())
aioble.Characteristic(device_info, bluetooth.UUID(HARDWARE_REVISION_ID), read=True, initial=sys.version)
aioble.Characteristic(device_info, bluetooth.UUID(BLE_VERSION_ID), read=True, initial="unknown")

