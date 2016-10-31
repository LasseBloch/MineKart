from signal import *
import RPi.GPIO as GPIO
import sys
import time

motor_a_pin1 = 17
motor_a_pin2 = 27

motor_b_pin1 = 23
motor_b_pin2 = 24

def main(argv):

    for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
        signal(sig, clean)

    setup_gpio();
    while True:
        print "forward"
        control_motors('F', 'F')
        time.sleep(3)
        print "A forward"
        control_motors('F', 'S')
        time.sleep(3)
        print "A backward"
        control_motors('B', 'S')
        time.sleep(3)
        print "B forward"
        control_motors('S', 'F')
        time.sleep(3)
        print "B backward"
        control_motors('S', 'F')
        time.sleep(3)
        print "backwards"
        control_motors('S', 'F')
        time.sleep(3)


def clean(*args):
    GPIO.output(motor_b_pin1, GPIO.LOW)
    GPIO.output(motor_b_pin2, GPIO.LOW)
    GPIO.output(motor_a_pin1, GPIO.LOW)
    GPIO.output(motor_a_pin2, GPIO.LOW)
    sys.exit(0)




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
    else:
        GPIO.output(motor_a_pin1, GPIO.LOW)
        GPIO.output(motor_a_pin2, GPIO.LOW)

    if motor_b_direction == 'F':
        GPIO.output(motor_b_pin1, GPIO.HIGH)
        GPIO.output(motor_b_pin2, GPIO.LOW)
    elif motor_b_direction == 'B':
        GPIO.output(motor_b_pin1, GPIO.LOW)
        GPIO.output(motor_b_pin2, GPIO.HIGH)
    else:
        GPIO.output(motor_b_pin1, GPIO.LOW)
        GPIO.output(motor_b_pin2, GPIO.LOW)

if __name__ == "__main__":
   main(sys.argv[1:])
