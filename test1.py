import RPi.GPIO as GPIO
import time

# Define GPIO pins for TB6612 H-bridge (front wheels)
DIR1_Front = 22  # Direction control for front left motor
PWM1_Front = 6  # Speed control for front left motor

DIR2_Front = 0  # Direction control for front right motor
PWM2_Front = 12  # Speed control for front right motor

# Define GPIO pins for TB6612 H-bridge (back wheels)
DIR1_Back = 3  # Direction control for back left motor
PWM1_Back = 24  # Speed control for back left motor

DIR2_Back = 14  # Direction control for back right motor
PWM2_Back = 10  # Speed control for back right motor

# Define GPIO pins for line sensors
SENSOR_LEFT = 18  # Left line sensor
SENSOR_RIGHT = 22  # Right line sensor

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)

GPIO.setup(DIR1_Front, GPIO.OUT)
GPIO.setup(PWM1_Front, GPIO.OUT)
GPIO.setup(DIR2_Front, GPIO.OUT)
GPIO.setup(PWM2_Front, GPIO.OUT)

GPIO.setup(DIR1_Back, GPIO.OUT)
GPIO.setup(PWM1_Back, GPIO.OUT)
GPIO.setup(DIR2_Back, GPIO.OUT)
GPIO.setup(PWM2_Back, GPIO.OUT)

GPIO.setup(SENSOR_LEFT, GPIO.IN)
GPIO.setup(SENSOR_RIGHT, GPIO.IN)

# Create PWM objects for speed control
pwm_front_left = GPIO.PWM(PWM1_Front, 100)  # 100Hz for front left motor
pwm_front_right = GPIO.PWM(PWM2_Front, 100)  # 100Hz for front right motor
pwm_back_left = GPIO.PWM(PWM1_Back, 100)  # 100Hz for back left motor
pwm_back_right = GPIO.PWM(PWM2_Back, 100)  # 100Hz for back right motor

# Start PWM with 50% duty cycle
pwm_front_left.start(0)
pwm_front_right.start(0)
pwm_back_left.start(0)
pwm_back_right.start(0)

# Functions to control motors
def move_forward():
    # Set direction to forward
    GPIO.output(DIR1_Front, GPIO.HIGH)
    GPIO.output(DIR2_Front, GPIO.HIGH)
    GPIO.output(DIR1_Back, GPIO.LOW)
    GPIO.output(DIR2_Back, GPIO.LOW)

def move_backward():
    # Set direction to backward
    GPIO.output(DIR1_Front, False)
    GPIO.output(DIR2_Front, False)
    GPIO.output(DIR1_Back, False)
    GPIO.output(DIR2_Back, False)

def stop_motors():
    # Stop motors
    pwm_front_left.ChangeDutyCycle(0)
    pwm_front_right.ChangeDutyCycle(0)
    pwm_back_left.ChangeDutyCycle(0)
    pwm_back_right.ChangeDutyCycle(0)

def set_speed(left_speed, right_speed):
    # Adjust speed for left and right sides
    pwm_front_left.ChangeDutyCycle(left_speed)
    pwm_front_right.ChangeDutyCycle(right_speed)
    pwm_back_left.ChangeDutyCycle(left_speed)
    pwm_back_right.ChangeDutyCycle(right_speed)

# Line following logic
while True:
    # Read sensor data
    sensor_left_reading = GPIO.input(SENSOR_LEFT)
    sensor_right_reading = GPIO.input(SENSOR_RIGHT)

    # Increase sensor sensitivity by using a threshold value
    threshold = 500  # Adjust this value to increase/decrease sensor sensitivity
    if sensor_left_reading < threshold:
        sensor_left_reading = 0
    else:
        sensor_left_reading = 1

    if sensor_right_reading < threshold:
        sensor_right_reading = 0
    else:
        sensor_right_reading = 1

    # If left sensor detects line, turn right and stop left motor
    if sensor_left_reading == 0:
        set_speed(0, 100)  # Stop left motor and turn right
    # If right sensor detects line, turn left and stop right motor
    elif sensor_right_reading == 0:
        set_speed(100, 0)  # Stop right motor and turn left
    # If both sensors detect line, move forward
    elif sensor_left_reading == 1 and sensor_right_reading == 1:
        move_forward()
        set_speed(100, 100)  # Move forward with full speed
    # If neither sensor detects line, stop
    else:
        stop_motors()

    # Wait for a short period before repeating
    time.sleep(0.05)