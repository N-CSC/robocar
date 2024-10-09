import RPi.GPIO as GPIO
import time

# Definer GPIO pins for TB6612 H-broer (forreste hjul)
DIR1_Front = 17  # Retningskontrol forreste venstre motor
PWM1_Front = 12  # Hastighedskontrol forreste venstre motor

DIR2_Front = 27  # Retningskontrol forreste højre motor
PWM2_Front = 13  # Hastighedskontrol forreste højre motor

# Definer GPIO pins for TB6612 H-broer (bageste hjul)
#DIR1_Back = 5  # Retningskontrol bageste venstre motor
#PWM1_Back = 18  # Hastighedskontrol bageste venstre motor

#DIR2_Back = 6  # Retningskontrol bageste højre motor
#PWM2_Back = 19  # Hastighedskontrol bageste højre motor

# Opsæt GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR1_Front, GPIO.OUT)
GPIO.setup(PWM1_Front, GPIO.OUT)
GPIO.setup(DIR2_Front, GPIO.OUT)
GPIO.setup(PWM2_Front, GPIO.OUT)

#GPIO.setup(DIR1_Back, GPIO.OUT)
#GPIO.setup(PWM1_Back, GPIO.OUT)
#GPIO.setup(DIR2_Back, GPIO.OUT)
#GPIO.setup(PWM2_Back, GPIO.OUT)

# Opret PWM objekter til hastighedskontrol
pwm_front_left = GPIO.PWM(PWM1_Front, 100)  # 100Hz til venstre forreste motor
pwm_front_right = GPIO.PWM(PWM2_Front, 100)  # 100Hz til højre forreste motor
#pwm_back_left = GPIO.PWM(PWM1_Back, 100)  # 100Hz til venstre bageste motor
#pwm_back_right = GPIO.PWM(PWM2_Back, 100)  # 100Hz til højre bageste motor

# Start PWM med 50% duty cycle
pwm_front_left.start(50)
pwm_front_right.start(50)
#pwm_back_left.start(50)
#pwm_back_right.start(50)

# Funktioner til at styre motorerne
def move_forward():
    # Sæt retningen til fremad
    GPIO.output(DIR1_Front, True)
    GPIO.output(DIR2_Front, True)
    #GPIO.output(DIR1_Back, True)
   # GPIO.output(DIR2_Back, True)

def move_backward():
    # Sæt retningen til baglæns
    GPIO.output(DIR1_Front, False)
    GPIO.output(DIR2_Front, False)
   # GPIO.output(DIR1_Back, False)
   # GPIO.output(DIR2_Back, False)

def stop_motors():
    # Stop motorerne
    pwm_front_left.ChangeDutyCycle(0)
    pwm_front_right.ChangeDutyCycle(0)
    #pwm_back_left.ChangeDutyCycle(0)
    #pwm_back_right.ChangeDutyCycle(0)

def set_speed(left_speed, right_speed):
    # Juster hastighed for venstre og højre side
    pwm_front_left.ChangeDutyCycle(left_speed)
    pwm_front_right.ChangeDutyCycle(right_speed)
    #pwm_back_left.ChangeDutyCycle(left_speed)
    #pwm_back_right.ChangeDutyCycle(right_speed)

# Testkørsel
try:
    while True:
        move_forward()
        set_speed(100, 100)  # Kør fremad med 75% hastighed
        time.sleep(1000)
        
        move_backward()
        set_speed(50, 50)  # Kør baglæns med 50% hastighed
        time.sleep(1000)

except KeyboardInterrupt:
    pwm_front_left.stop()
    pwm_front_right.stop()
    #pwm_back_left.stop()
    #pwm_back_right.stop()
    GPIO.cleanup()


