from sshkeyboard import listen_keyboard
import RPi.GPIO as GPIO
import time

# ... (rest of the code remains the same until the motor control functions)

def GoForward():
    set_individual_speeds(60, 60, 60, 60)  # forward

def GoBackward():
    set_individual_speeds(-60, -60, -60, -60)  # backward

def TurnLeft():
    set_individual_speeds(0, 80, 0, 80)  # left

def TurnRight():
    set_individual_speeds(80, 0, 80, 0)  # right

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

while True:
    try:
        listen_keyboard(on_press=press, on_release=release)
    except KeyboardInterrupt:
        pwm_front_left.stop()
        pwm_front_right.stop()
        pwm_back_left.stop()
        pwm_back_right.stop()
        GPIO.cleanup()
        print("Program stoppet og GPIO ryddet op.")