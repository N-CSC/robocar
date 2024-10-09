import RPi.GPIO as GPIO
import time

# Indstil GPIO pins for sensor inputs
left_sensor = 17  # Venstre sensor til GPIO17
right_sensor = 27  # Højre sensor til GPIO27

# Indstil GPIO til motor styring
motor_left_forward = 22
motor_left_backward = 23
motor_right_forward = 24
motor_right_backward = 25

# Opsæt GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(left_sensor, GPIO.IN)
GPIO.setup(right_sensor, GPIO.IN)
GPIO.setup(motor_left_forward, GPIO.OUT)
GPIO.setup(motor_left_backward, GPIO.OUT)
GPIO.setup(motor_right_forward, GPIO.OUT)
GPIO.setup(motor_right_backward, GPIO.OUT)

def move_forward():
    GPIO.output(motor_left_forward, True)
    GPIO.output(motor_left_backward, False)
    GPIO.output(motor_right_forward, True)
    GPIO.output(motor_right_backward, False)

def turn_left():
    GPIO.output(motor_left_forward, False)
    GPIO.output(motor_left_backward, True)
    GPIO.output(motor_right_forward, True)
    GPIO.output(motor_right_backward, False)

def turn_right():
    GPIO.output(motor_left_forward, True)
    GPIO.output(motor_left_backward, False)
    GPIO.output(motor_right_forward, False)
    GPIO.output(motor_right_backward, True)

def stop():
    GPIO.output(motor_left_forward, False)
    GPIO.output(motor_left_backward, False)
    GPIO.output(motor_right_forward, False)
    GPIO.output(motor_right_backward, False)

try:
    while True:
        left = GPIO.input(left_sensor)
        right = GPIO.input(right_sensor)
        
        if left == 1 and right == 1:
            move_forward()
        elif left == 0 and right == 1:
            turn_left()
        elif left == 1 and right == 0:
            turn_right()
        else:
            stop()
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
