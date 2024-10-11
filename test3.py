from sshkeyboard import listen_keyboard
import RPi.GPIO as GPIO
import time

# Definer GPIO pins for TCRT5000 sensorerne
left_sensor = 15  # GPIO pin til venstre sensor
right_sensor = 23  # GPIO pin til højre sensor

# Definer GPIO pins for TB6612 H-broer (forreste hjul)
DIR1_Front = 22  # Retningskontrol forreste venstre motor
PWM1_Front = 6   # Hastighedskontrol forreste venstre motor

DIR2_Front = 0   # Retningskontrol forreste højre motor
PWM2_Front = 12  # Hastighedskontrol forreste højre motor

# Definer GPIO pins for TB6612 H-broer (bageste hjul)
DIR1_Back = 3    # Retningskontrol bageste venstre motor
PWM1_Back = 24   # Hastighedskontrol bageste venstre motor

DIR2_Back = 14   # Retningskontrol bageste højre motor
PWM2_Back = 10    # Hastighedskontrol bageste højre motor

# Opsæt GPIO pins som input for sensorerne og output for motorerne
GPIO.setmode(GPIO.BCM)
GPIO.setup(left_sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Pulldown-modstand
GPIO.setup(right_sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Pulldown-modstand

GPIO.setup(DIR1_Front, GPIO.OUT)
GPIO.setup(PWM1_Front, GPIO.OUT)
GPIO.setup(DIR2_Front, GPIO.OUT)
GPIO.setup(PWM2_Front, GPIO.OUT)

GPIO.setup(DIR1_Back, GPIO.OUT)
GPIO.setup(PWM1_Back, GPIO.OUT)
GPIO.setup(DIR2_Back, GPIO.OUT)
GPIO.setup(PWM2_Back, GPIO.OUT)

# Opret PWM objekter til hastighedskontrol (100Hz frekvens)
pwm_front_left = GPIO.PWM(PWM1_Front, 1000)
pwm_front_right = GPIO.PWM(PWM2_Front, 1000)
pwm_back_left = GPIO.PWM(PWM1_Back, 1000)
pwm_back_right = GPIO.PWM(PWM2_Back, 1000)

# Start PWM med 0% duty cycle
pwm_front_left.start(0)
pwm_front_right.start(0)
pwm_back_left.start(0)
pwm_back_right.start(0)

# Funktioner til motorstyring
def set_individual_speeds(front_left_speed, front_right_speed, back_left_speed, back_right_speed):
    # Juster hastigheder individuelt for hver motor og reducer med 10%
    pwm_front_left.ChangeDutyCycle(front_left_speed * 0.9)  # 90% af max hastighed
    pwm_front_right.ChangeDutyCycle(front_right_speed * 0.9)  # 90% af max hastighed
    pwm_back_left.ChangeDutyCycle(back_left_speed * 0.9)  # 90% af max hastighed
    pwm_back_right.ChangeDutyCycle(back_right_speed * 0.9)  # 90% af max hastighed

def stop_motors():
    # Stop alle motorer
    pwm_front_left.ChangeDutyCycle(0)
    pwm_front_right.ChangeDutyCycle(0)
    pwm_back_left.ChangeDutyCycle(0)
    pwm_back_right.ChangeDutyCycle(0)


def GoForward():
    print("going forward")

def GoBackward():
    print("going backward")

def TurnLeft():
    print("turning left")

def TurnRight():
    print("turning right")

def Stop():
    print("stopping")

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
    listen_keyboard(on_press=press, on_release=release)


     
