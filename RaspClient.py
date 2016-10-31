#!/usr/bin/python
import cv2
import binascii
import struct
import numpy as np
import sys
import socket
import time
import RPi.GPIO as GPIO
from signal import *


cap = cv2.VideoCapture(0)

motor_a_pin1 = 17
motor_a_pin2 = 27

motor_b_pin1 = 23
motor_b_pin2 = 24



def main(argv):
    if (len(sys.argv) != 3):
        print "You must provide two arguments: ip port"
    else:
        for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
            signal(sig, clean)
        setup_gpio()
        destination = str(sys.argv[1])
        port = int(sys.argv[2])
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (destination, port)
        print "server_address: ", server_address
        sock.connect(server_address)
        while True:
            data = sock.recv(16)
            motor_a_direction = data[0]
            motor_b_direction = data[1]
            print "motor A direction: ", motor_a_direction
            print "motor B direction: ", motor_b_direction
            control_motors(motor_a_direction, motor_b_direction)
            print "Send picture"
            pic = pack_image(80,60)
            sock.sendall(pic)
            data = ""


def pack_image(width, height):
       # Capture frame-by-frame
       ret = 0
       frame = 0
       for n in range(0,5):
           ret, frame = cap.read()
       if (ret):
           small_image = cv2.resize(frame, (width, height))
           flat_img = small_image.flatten()
           flat_img_list = flat_img.tolist()
           size_metadata = (width, height)
           s = struct.Struct('I I')
           testPack = s.pack(*size_metadata)
           testPack += struct.pack('B'*len(flat_img_list), *flat_img_list)
           return testPack


def setup_gpio():
    GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
    GPIO.setup(motor_a_pin1, GPIO.OUT)
    GPIO.setup(motor_a_pin2, GPIO.OUT)
    GPIO.setup(motor_b_pin1, GPIO.OUT)
    GPIO.setup(motor_b_pin2, GPIO.OUT)


def control_motors(motor_a_direction, motor_b_direction):

    if motor_a_direction == 'F':
        GPIO.output(motor_a_pin1, GPIO.HIGH)
        GPIO.output(motor_a_pin2, GPIO.LOW)
    elif motor_a_direction == 'B':
        GPIO.output(motor_a_pin1, GPIO.LOW)
        GPIO.output(motor_a_pin2, GPIO.HIGH)
    else # stop
        GPIO.output(motor_a_pin1, GPIO.LOW)
        GPIO.output(motor_a_pin2, GPIO.LOW)

    if motor_b_direction == 'F':
        GPIO.output(motor_b_pin1, GPIO.HIGH)
        GPIO.output(motor_b_pin2, GPIO.LOW)
    elif motor_b_direction == 'B':
        GPIO.output(motor_b_pin1, GPIO.LOW)
        GPIO.output(motor_b_pin2, GPIO.HIGH)
    else #Stop
        GPIO.output(motor_b_pin1, GPIO.LOW)
        GPIO.output(motor_b_pin2, GPIO.LOW)

def clean(*args):
    GPIO.output(motor_b_pin1, GPIO.LOW)
    GPIO.output(motor_b_pin2, GPIO.LOW)
    GPIO.output(motor_a_pin1, GPIO.LOW)
    GPIO.output(motor_a_pin2, GPIO.LOW)
    sys.exit(0)


if __name__ == "__main__":
   main(sys.argv[1:])
