import RPi.GPIO as GPIO
import time

# Definer pins
DIR1 = 20  # Retning for motor 1
PWM1 = 21  # Hastighed for motor 1
DIR2 = 19  # Retning for motor 2
PWM2 = 26  # Hastighed for motor 2

# Sæt op GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR1, GPIO.OUT)
GPIO.setup(PWM1, GPIO.OUT)
GPIO.setup(DIR2, GPIO.OUT)
GPIO.setup(PWM2, GPIO.OUT)

# Start PWM
pwm1 = GPIO.PWM(PWM1, 100)  # 100 Hz
pwm2 = GPIO.PWM(PWM2, 100)  # 100 Hz
pwm1.start(0)
pwm2.start(0)

# Test motor 1
#GPIO.output(DIR1, GPIO.HIGH)  # Sæt retning
#pwm1.ChangeDutyCycle(100)  # 100% hastighed
#time.sleep(5)  # Kør i 5 sekunder
#pwm1.ChangeDutyCycle(0)  # Stop motor

# Test motor 2
GPIO.output(DIR2, GPIO.HIGH)  # Sæt retning
pwm2.ChangeDutyCycle(100)  # 100% hastighed
time.sleep(5)  # Kør i 5 sekunder
pwm2.ChangeDutyCycle(0)  # Stop motor

# Ryd GPIO
GPIO.cleanup()
