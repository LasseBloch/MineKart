#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import cv2
import binascii
import struct
import numpy as np
import sys
import socket
from mc import *

mc = Minecraft()
width = 80
height = 60
x = 0
y = 0
z = 0


class McPictureDrawer:

    COLORS = ( (35,0, 222,222,222), # ID: 35 = Wool
		(35,1, 219,125,63),
		(35,2, 180,81,189),
		(35,3, 107,138,201),
		(35,4, 177,166,39),
		(35,5, 66,174,57),
		(35,6, 208,132,153),
		(35,7, 64,64,64),
		(35,8, 155,161,161),
		(35,9, 47,111,137),
		(35,10, 127,62,182),
		(35,11, 46,57,142),
		(35,12, 79,50,31),
		(35,13, 53,71,27),
		(35,14, 151,52,49),
		(35,15, 26,22,22),
        (159,0,210,178,161), # ID: 159 = Clay
		(159,1,162,84,38),
		(159,2,150,88,109),
		(159,3,113,109,138),
		(159,4,186,133,35),
		(159,5,104,118,53),
		(159,6,162,78,79),
		(159,7,58,42,36),
		(159,8,135,107,98),
		(159,9,87,91,91),
		(159,10,118,70,86),
		(159,11,74,60,91),
		(159,12,77,51,36),
		(159,13,76,83,42),
		(159,14,143,61,47),
		(159,15,37,23,16),
        (155,0,232,228,220), # ID: 155 = Quartz
        (152,0,164,26,9), # ID: 152 = Redstone
        (41,0,250,239,80), # ID: Gold block
        (173,0,19,19,19) ) # ID: Coal Block

    def __init__(self, mc_):
        self.mc = mc_
        self.width = 80
        self.height = 60
        self.x = 0
        self.y = 0
        self.z = 0

    def setPicturePosition(self, x_, y_, z_):
        self.x = x_
        self.y = y_
        self.z = z_

    """
    dR*dR + dB*dB + dG*dG
    rgb -> bgr
    """
    def colorDist(self, a,b):
        return (a[0]-b[2])*(a[0]-b[2])+(a[1]-b[1])*(a[1]-b[1])+(a[2]-b[0])*(a[2]-b[0])

    def getBestColor(self, rgb):
        bestColor = self.COLORS[-1]
        bestDist = 255*255*3
        for c in self.COLORS:
            d = self.colorDist(c[2:],rgb)
            if d < bestDist:
                bestDist = d
                bestColor = c
        return bestColor

    def drawCompletePicture(self, img):
        for y in range(self.height):
            for x in range(self.width):
                block = self.getBestColor(img[y][x])[0:2]
                mc.setBlock(self.x - x, self.y+height-1-y, self.z, block)



def main():
	port = 2253
	pos = mc.player.getTilePos()
    pos.x = -10
    pos.y = 0
    pos.z = -10
        
	width = 80
	height = 60

	dut = McPictureDrawer(mc)
	dut.setPicturePosition(pos.x + (width/2), pos.y, pos.z + 30)


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('', port)
    sock.bind(server_address)
    while True:
        # wait for connection
        mc.postToChat("Waiting for connection")
        sock.listen(1)
        connection, client_address = sock.accept()
        mc.postToChat("READY TO ROLL!!!")
        while True:

            car_cmd = "00"
            engine_on = False

            # get latest command
            with open(LOG_FILE) as fd:
                log_data = fd.read()
                # Strip all but latest 20 char
                latest = log_data[ len(log_data) - 10: ].lower()

                # Search for commands
                forward_idx = latest.find("#forward")
                reverse_idx = latest.find("#reverse")
                right_idx = latest.find("###right")
                left_idx = latest.find("####left")
                key_idx = latest.find("#####key")

                if( forward_idx >= 0 and reverse_idx < 0 and right_idx < 0 and left_idx < 0 key_idx < 0 ):
                    if( engine_on ):
                        car_cmd = "FF"
                    else:
                        car_cmd = "00"
                elif( forward_idx < 0 and reverse_idx >= 0 and right_idx < 0 and left_idx < 0 key_idx < 0 ):
                    if( engine_on ):
                        car_cmd = "BB"
                    else:
                        car_cmd = "00"
                elif( forward_idx < 0 and reverse_idx < 0 and right_idx >= 0 and left_idx < 0 key_idx < 0 ):
                    if( engine_on ):
                        car_cmd = "0F"
                    else:
                        car_cmd = "00"
                elif( forward_idx < 0 and reverse_idx < 0 and right_idx < 0 and left_idx >= 0 key_idx < 0 ):
                    if( engine_on ):
                        car_cmd = "F0"
                    else:
                        car_cmd = "00"
                elif( forward_idx < 0 and reverse_idx < 0 and right_idx < 0 and left_idx < 0 key_idx >= 0 ):
                    car_cmd = "00"
                    if( engine_on ):
                        mc.postToChat("Engine off")
                        engine_on = False
                    else:
                        engine_on = True
                        mc.postToChat("Engine on")

            connection.sendall(car_cmd)
            data = connection.recv(8)
            assembled_size_metadata = struct.unpack('I I', data[0:8])

            assembled_image_size = assembled_size_metadata[0] * assembled_size_metadata[1] * 3
            # try to read the rest of the picture
            while len(data) < assembled_image_size:
                data += connection.recv(1024)
            res = unpack_image(data)

            dut.drawCompletePicture(res)


def unpack_image(packed_image):
    assembled_size_metadata = struct.unpack('I I', packed_image[0:8])
    assembled_image_size = assembled_size_metadata[0] * assembled_size_metadata[1] * 3

    convertedBack = struct.unpack('B'*assembled_image_size, packed_image[8:])

    testnp = np.asarray(convertedBack, dtype=np.uint8)

    assembledImg = np.reshape(testnp, (assembled_size_metadata[1], assembled_size_metadata[0], 3))
	return assembledImg

if __name__ == "__main__":
   main()
