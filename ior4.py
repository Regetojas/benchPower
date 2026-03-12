#!/home/dglass/pythonic/benchPower/venv/bin/python
# -*- coding: utf-8 -*-
"""
Command-line executable python script to control DLP-IOR4 latching relay

"""

import serial
import serial.tools.list_ports
import time
import sys

BAUD_RATE = 9600
PRODUCT_ID = "DLP-IOR4"

def get_serial_port():
    device = None
    for port in serial.tools.list_ports.comports():
        if PRODUCT_ID in str(port.product):
            device = port.device
            print(f"Found {PRODUCT_ID} at {device}")
            break
    if device == None:
        print(f"{PRODUCT_ID} not found")
    return device


def main():

    device = get_serial_port()
    try:
        with serial.Serial(device, BAUD_RATE, timeout=1) as ser:
            print(f"Opened serial port: {ser.name}")
            if len(sys.argv) > 1:
                command_arg = sys.argv[1]
            else:
                command_arg = ""
    
            arg_low = command_arg.lower()
    
            if "1a" in arg_low:
                ser.write(b'1')
                print("Connected terminal 1 to A")
            elif "1b" in arg_low:
                ser.write(b'Q')
                print("Connected terminal 1 to B")
            elif "2a" in arg_low:
                ser.write(b'2')
                print("Connected terminal 2 to A")
            elif "2" in arg_low:
                ser.write(b'W')
                print("Connected terminal 2 to B")
            elif "3a" in arg_low:
                ser.write(b'3')
                print("Connected terminal 3 to A")
            elif "3b" in arg_low:
                ser.write(b'E')
                print("Connected terminal 3 to B")
            elif "4a" in arg_low:
                ser.write(b'4')
                print("Connected terminal 4 to A")
            elif "4b" in arg_low:
                ser.write(b'R')
                print("Connected terminal 4 to B")
            elif "ping" in arg_low:
                ser.write(b"'")
                pong = ser.read(1)
                if pong == b'R':
                    print(f"{device} returned {pong}, ping success")
                else:
                    print(f"ping failed")
            else:
                print("Invalid Command Argument")
                print("usage: io4.py 1a|1b|2a|2b|3a|3b|4a|4b|ping")
               
    except serial.SerialException as e:
            print(f"ERROR opening serial port: {e}")

    except Exception as e:
            print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
            
