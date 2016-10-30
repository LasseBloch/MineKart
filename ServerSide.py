#!/usr/bin/python
import cv2
import binascii
import struct
import numpy as np
import sys
import socket
import time

def main(argv):
    if (len(sys.argv) != 2):
        print "You must provide one argument: port"
    else:
        print "test"
        port = int(sys.argv[1])
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('', port)
        sock.bind(server_address)
        while True:
            # wait for connection
            print "Waiting for connection"
            sock.listen(1)
            connection, client_address = sock.accept()
            print client_address, "Got connection"
            while True:
                connection.sendall('1')
                data = connection.recv(8)
                assembled_size_metadata = struct.unpack('I I', data[0:8])
                print "ass size: ", assembled_size_metadata
                assembled_image_size = assembled_size_metadata[0] * assembled_size_metadata[1] * 3
                # try to read the rest of the picture
                while len(data) < assembled_image_size:
                    data += connection.recv(1024)
                unpack_image(data)
            break

def unpack_image(packed_image):
        print len(packed_image)
        assembled_size_metadata = struct.unpack('I I', packed_image[0:8])
        assembled_image_size = assembled_size_metadata[0] * assembled_size_metadata[1] * 3
        print 'ass size, ', assembled_image_size
        print "testpack lenght", len(packed_image[8:])
        convertedBack = struct.unpack('B'*assembled_image_size, packed_image[8:])
        testnp = np.asarray(convertedBack, dtype=np.uint8)
        #print testnp.shape
        #print "size of testnp", len(testnp)

        assembledImg = np.reshape(testnp, (assembled_size_metadata[1], assembled_size_metadata[0], 3))
        cv2.imshow('Frame', assembledImg)
        #cv2.imwrite( "LAL.jpg", assembledImg)
        cv2.waitKey(1)


if __name__ == "__main__":
   main(sys.argv[1:])
