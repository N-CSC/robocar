from sshkeyboard import listen_keyboard
import RPi.GPIO as GPIO
import time

# Set up GPIO pins for motor control
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for motor control
DIR1_Front = 22  # Direction control for front left motor
PWM1_Front = 6   # Speed control for front left motor

DIR2_Front = 0   # Direction control for front right motor
PWM2_Front = 12  # Speed control for front right motor

DIR1_Back = 3    # Direction control for back left motor
PWM1_Back = 24   # Speed control for back left motor

DIR2_Back = 14   # Direction control for back right motor
PWM2_Back = 10   # Speed control for back right motor

# Set up GPIO pins as output for motor control
GPIO.setup(DIR1_Front, GPIO.OUT)
GPIO.setup(PWM1_Front, GPIO.OUT)
GPIO.setup(DIR2_Front, GPIO.OUT)
GPIO.setup(PWM2_Front, GPIO.OUT)

GPIO.setup(DIR1_Back, GPIO.OUT)
GPIO.setup(PWM1_Back, GPIO.OUT)
GPIO.setup(DIR2_Back, GPIO.OUT)
GPIO.setup(PWM2_Back, GPIO.OUT)

# Create PWM objects for speed control
pwm_front_left = GPIO.PWM(PWM1_Front, 1000)
pwm_front_right = GPIO.PWM(PWM2_Front, 1000)
pwm_back_left = GPIO.PWM(PWM1_Back, 1000)
pwm_back_right = GPIO.PWM(PWM2_Back, 1000)

# Start PWM with 0% duty cycle
pwm_front_left.start(0)
pwm_front_right.start(0)
pwm_back_left.start(0)
pwm_back_right.start(0)

# Define functions for motor control
def set_individual_speeds(front_left_speed, front_right_speed, back_left_speed, back_right_speed):
    pwm_front_left.ChangeDutyCycle(front_left_speed * 0.9)  # 90% of max speed
    pwm_front_right.ChangeDutyCycle(front_right_speed * 0.9)  # 90% of max speed
    pwm_back_left.ChangeDutyCycle(back_left_speed * 0.9)  # 90% of max speed
    pwm_back_right.ChangeDutyCycle(back_right_speed * 0.9)  # 90% of max speed

def stop_motors():
    pwm_front_left.ChangeDutyCycle(0)
    pwm_front_right.ChangeDutyCycle(0)
    pwm_back_left.ChangeDutyCycle(0)
    pwm_back_right.ChangeDutyCycle(0)

# Define functions for keyboard events
def GoForward():
    set_individual_speeds(100, 100, 100, 100)  # forward

def GoBackward():
    set_individual_speeds(-70, -70, -70, -70)  # backward

def TurnLeft():
    set_individual_speeds(0, 100, 0, 100)  # left

def TurnRight():
    set_individual_speeds(100, 0, 100, 0)  # right

def Stop():
    stop_motors()  # stop

def press(key):
    if key == "w":
        GoForward()
    elif key == "s":
        GoBackward()
    elif key == "a":
        TurnLeft()
    elif key == "d":
        TurnRight()
    elif key == "space":
        Stop()

def release(key):
    if key == "w" or key == "s" or key == "a" or key == "d" or key == "space":
        Stop()

# Start listening for keyboard events
while True:
    try:
        listen_keyboard(on_press=press, on_release=release)
    except KeyboardInterrupt:
        pwm_front_left.stop()
        pwm_front_right.stop()
        pwm_back_left.stop()
        pwm_back_right.stop()
        GPIO.cleanup()
        print("Program stopped and GPIO cleaned up.")