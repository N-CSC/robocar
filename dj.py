import RPi.GPIO as GPIO
import time

# Pin-konfiguration
left_sensor = 17  # Venstre sensor til GPIO17
right_sensor = 27  # Højre sensor til GPIO27

# Motor driver pins
IN1 = 22  # Motor 1 retning
IN2 = 23  # Motor 1 retning
IN3 = 24  # Motor 2 retning
IN4 = 25  # Motor 2 retning
ENA = 12  # PWM til motor 1 hastighed
ENB = 13  # PWM til motor 2 hastighed

# Opsæt GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(left_sensor, GPIO.IN)
GPIO.setup(right_sensor, GPIO.IN)

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

# Opret PWM objekter
pwm_left = GPIO.PWM(ENA, 100)  # 100Hz PWM signal til venstre motor
pwm_right = GPIO.PWM(ENB, 100)  # 100Hz PWM signal til højre motor

# Start PWM ved 50% duty cycle
pwm_left.start(50)
pwm_right.start(50)

def move_forward():
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)

def turn_left():
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)

def turn_right():
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)

def stop():
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, False)

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
    pwm_left.stop()
    pwm_right.stop()
    GPIO.cleanup()
