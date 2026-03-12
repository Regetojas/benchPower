#!/home/dglass/pythonic/benchPower/venv/bin/python
# -*- coding: utf-8 -*-

import pyvisa
import time
import sys 

def list_query_strings(rm):
    resources = rm.list_resources()
    for resource_name in resources:
        try:
            inst = rm.open_resource(resource_name)
            inst.timeout = 2000  # set timeout to 2000 millisec
            idn_response = inst.query("*IDN?").strip()
            print(f"Found {idn_response} at {resource_name}")
            inst.close()
        except Exception as e:
            continue

        

def get_inst_by_idn(rm, target_idn_string):

    resources = rm.list_resources()

    for resource_name in resources:
        try:
            inst = rm.open_resource(resource_name)
            inst.timeout = 2000  # set timeout to 2000 millisec
            idn_response = inst.query("*IDN?").strip()
            inst.close()
            if target_idn_string in idn_response:
                print(f"Found {idn_response} at {resource_name}")
                return resource_name
        except Exception as e:
            continue
    print(f"No instrument with {target_idn_string} found")
    return None

def bench_on(benchSupply):
    # Set voltage in Volts
    benchSupply.write("VOLT 20.0") 
    # Set current limit in Amps
    benchSupply.write("CURR 1.5") 
    # Enable the output
    benchSupply.write("OUTPUT ON") 
    print("Set output to 20V, 1.5A, and enabled output.")

def bench_measure(benchSupply):
    actual_voltage = float(benchSupply.query("MEAS:VOLT?").strip())
    actual_current = float(benchSupply.query("MEAS:CURR?").strip())
    print(f"Measured Voltage: {actual_voltage:.3f} V")
    print(f"Measured Current: {actual_current:.3f} A")

def bench_off(benchSupply):
    benchSupply.write("OUTPUT OFF")
    print("Output disabled.")


def main():
    if len(sys.argv) > 1:
        command_arg = sys.argv[1]
    else:
        command_arg = ""
    
    arg_low = command_arg.lower()


    # 1. Initialize the Resource Manager
    # The rm variable is the gateway to all connected instruments.
    rm = pyvisa.ResourceManager("@py") # Use '@py' for the pure Python backend
    if "que" in arg_low:
        list_query_strings(rm)
        return
    
    # Get visa resource for the power supply
    #benchSupplyResource = get_inst_by_idn(rm, 'E3644A')
    benchSupplyResource = get_inst_by_idn(rm, 'DP832')

    if benchSupplyResource:
        try:
            # Open a connection to the instrument
            # Common serial settings: baud_rate=9600, data_bits=8, parity=NO_PARITY, stop_bits=STOP_BITS_ONE
            benchSupply = rm.open_resource(benchSupplyResource, baud_rate=9600, timeout=2000)
            print(f"Connection established with {benchSupplyResource}")

            # Communicate using SCPI commands
            # Query the device ID (*IDN? is a common standard command)
            idn = benchSupply.query("*IDN?")
            print(f"Instrument ID: {idn.strip()}") # .strip() removes leading/trailing whitespace and newline chars

            if "on" in arg_low:
                bench_on(benchSupply)
                time.sleep(1)
                bench_measure(benchSupply)
            elif "off" in arg_low: 
                bench_off(benchSupply)
                time.sleep(1)
                bench_measure(benchSupply)
            elif "meas" in arg_low:
                bench_measure(benchSupply)
            else:
                print(f"unknown command: {command_arg}")
                print(f"  valid commands are: on off measure")

            benchSupply.close()
            rm.close()

        except pyvisa.errors.VisaIOError as e:
            print(f"A VISA I/O error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
