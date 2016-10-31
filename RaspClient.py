#!/usr/bin/python
import cv2
import binascii
import struct
import numpy as np
import sys
import socket
import time

cap = cv2.VideoCapture(0)

def main(argv):
    if (len(sys.argv) != 3):
        print "You must provide two arguments: ip port"
    else:
        destination = str(sys.argv[1])
        port = int(sys.argv[2])
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (destination, port)
        print "server_address: ", server_address
        sock.connect(server_address)
        while True:
            data = sock.recv(8)
            print "data is ", data
            if (data == '1'):
                print "Send picture"
                pic = pack_image(80,60)
                sock.sendall(pic)
            data = ""

def pack_image(width, height):
       # Capture frame-by-frame
       ret = 0
       frame = 0
       for i in range(5):
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


if __name__ == "__main__":
   main(sys.argv[1:])
