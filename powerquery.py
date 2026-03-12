#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command-line executable python script to power up bench supply

"""

import serial
import time

SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

try:
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        print(f"Opened serial port: {ser.name}")

        command = b'*IDN?\n'
        ser.write(command)
        print(f"Sent data: {command.decode().strip()}")

        time.sleep(0.5)

        while True:
            response = ser.readline()
            if not response:
                break
            print(f"Received data: {response.decode().strip()}")

except serial.SerialException as e:
            print(f"ERROR opening serial port: {e}")

except Exception as e:
            print(f"ERROR: {e}")
