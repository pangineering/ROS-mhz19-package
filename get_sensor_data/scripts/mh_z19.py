#!/usr/bin/python3
# MIT License

# Copyright (c) 2019 JetsonHacksNano

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import Jetson.GPIO as GPIO
import time
import serial
import struct
import platform
import sys
import json
import os.path
import subprocess
import traceback



serial_dev = "/dev/ttyTHS1"
p_ver = platform.python_version_tuple()[0]

def connect_serial():
    serial_port = serial.Serial(
        port="/dev/ttyTHS1",
        baudrate=115200,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
    )
    # Wait a second to let the port initialize
    time.sleep(1)
    return serial_port


def read_concentration():
    retry_count = 3
    try:
        ser = connect_serial()
        for retry in range(retry_count):
            result=ser.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
            s=ser.read(9)

        if p_ver == '2':
            if len(s) >= 4 and s[0] == "\xff" and s[1] == "\x86" and checksum(s[1:-1]) == s[-1]:
                return ord(s[2])*256 + ord(s[3])
        else:
            if len(s) >= 4 and s[0] == 0xff and s[1] == 0x86 and ord(checksum(s[1:-1])) == s[-1]:
                return s[2]*256 + s[3]
    except:
        traceback.print_exc()
    return ""

def mh_z19():
  co2 = read_concentration()
  if not co2:
    return {}
  else:
    return {'co2': co2}


def checksum(array):
  if p_ver == '2' and isinstance(array, str):
    array = [ord(c) for c in array]
  csum = sum(array) % 0x100
  if csum == 0:
    return struct.pack('B', 0)
  else:
    return struct.pack('B', 0xff - csum + 1)

def read():


  result = mh_z19()

  return result