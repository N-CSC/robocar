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
PWM2_Back = 10   # Hastighedskontrol forreste højre motor

# Opsæt GPIO pins som input for sensorerne og output for motorerne
GPIO.setmode(GPIO.BCM)
GPIO.setup(left_sensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(right_sensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(DIR1_Front, GPIO.OUT)
GPIO.setup(PWM1_Front, GPIO.OUT)
GPIO.setup(DIR2_Front, GPIO.OUT)
GPIO.setup(PWM2_Front, GPIO.OUT)

GPIO.setup(DIR1_Back, GPIO.OUT)
GPIO.setup(PWM1_Back, GPIO.OUT)
GPIO.setup(DIR2_Back, GPIO.OUT)
GPIO.setup(PWM2_Back, GPIO.OUT)

# Opret PWM objekter til hastighedskontrol (100Hz frekvens)
pwm_front_left = GPIO.PWM(PWM1_Front, 100)
pwm_front_right = GPIO.PWM(PWM2_Front, 100)
pwm_back_left = GPIO.PWM(PWM1_Back, 100)
pwm_back_right = GPIO.PWM(PWM2_Back, 100)

# Start PWM med 0% duty cycle
pwm_front_left.start(0)
pwm_front_right.start(0)
pwm_back_left.start(0)
pwm_back_right.start(0)

# Funktioner til motorstyring
def move_forward():
    # Sæt retningen til fremad
    GPIO.output(DIR1_Front, GPIO.HIGH)
    GPIO.output(DIR2_Front, GPIO.HIGH)
    GPIO.output(DIR1_Back, GPIO.LOW)
    GPIO.output(DIR2_Back, GPIO.LOW)
    pwm_back_left.ChangeDutyCycle(70)
    pwm_back_right.ChangeDutyCycle(70)
    pwm_front_left.ChangeDutyCycle(70)
    pwm_front_right.ChangeDutyCycle(70)

def move_backward():
    # Sæt retningen til baglæns
    GPIO.output(DIR1_Front, GPIO.LOW)
    GPIO.output(DIR2_Front, GPIO.LOW)
    GPIO.output(DIR1_Back, GPIO.LOW)
    GPIO.output(DIR2_Back, GPIO.LOW)
    pwm_back_left.ChangeDutyCycle(50)
    pwm_back_right.ChangeDutyCycle(50)
    pwm_front_left.ChangeDutyCycle(50)
    pwm_front_right.ChangeDutyCycle(50)

def stop_motors():
    # Stop alle motorer
    pwm_front_left.ChangeDutyCycle(0)
    pwm_front_right.ChangeDutyCycle(0)
    pwm_back_left.ChangeDutyCycle(0)
    pwm_back_right.ChangeDutyCycle(0)

def set_speed(left_speed, right_speed):
    # Juster hastighed for venstre og højre side
    pwm_front_left.ChangeDutyCycle(left_speed)
    pwm_front_right.ChangeDutyCycle(right_speed)
    pwm_back_left.ChangeDutyCycle(left_speed)
    pwm_back_right.ChangeDutyCycle(right_speed)

# Hovedprogram til at styre motorer baseret på sensorer
'''
try:
    while True:
        # Læs sensorernes værdier
        left_value = GPIO.input(left_sensor)  # 0 = ingen refleksion (sort), 1 = refleksion (hvid tape)
        right_value = GPIO.input(right_sensor)

        # Udskriv sensorværdier til terminalen
        print(f"Venstre sensor: {left_value}, Højre sensor: {right_value}")

        # Motorstyring baseret på sensor-input (for eksempel linjefølgning)
        if left_value == 1 and right_value == 1:
            # Begge sensorer ser hvidt -> kør fremad
            move_forward()
        elif left_value == 0 and right_value == 1:
            # Venstre sensor ser sort, højre ser hvid -> drej til venstre
            set_speed(100, 50)  # Sænk venstre motorhastighed
        elif left_value == 1 and right_value == 0:
            # Venstre sensor ser hvid, højre ser sort -> drej til højre
            set_speed(50, 100)  # Sænk højre motorhastighed
        else:
            # Begge sensorer ser sort -> stop motorerne
            stop_motors()

        time.sleep(0.1)  # Vent lidt før næste aflæsning
        

except KeyboardInterrupt:
    # Stop motorer og ryd op når programmet afbrydes
    pwm_front_left.stop()
    pwm_front_right.stop()
    pwm_back_left.stop()
    pwm_back_right.stop()
    GPIO.cleanup()
    print("Program stoppet og GPIO ryddet op.")
    '''
try:
    while True:
        # Læs sensorernes værdier
        left_value = GPIO.input(left_sensor)  # 0 = ingen refleksion (sort), 1 = refleksion (hvid tape)
        right_value = GPIO.input(right_sensor)

        # Udskriv sensorværdier til terminalen
        print(f"Venstre sensor: {left_value}, Højre sensor: {right_value}")

        # Motorstyring baseret på sensor-input
        if left_value == 1 and right_value == 1:
            # Begge sensorer ser hvidt -> kør fremad, men sænk begge motorer
            set_speed(50, 50)  # Sænk begge motorers hastighed
        elif left_value == 1 and right_value == 0:
            # Venstre sensor ser hvid -> Sænk venstre motor
            set_speed(50, 100)  # Sænk venstre motor, højre kører fuld kraft
        elif left_value == 0 and right_value == 1:
            # Højre sensor ser hvid -> Sænk højre motor
            set_speed(100, 50)  # Højre motor sænkes, venstre kører fuld kraft
        else:
            # Begge sensorer ser sort -> kør fremad med fuld kraft
            set_speed(100, 100)  # Fuld hastighed på begge motorer

        time.sleep(0.1)  # Vent lidt før næste aflæsning

except KeyboardInterrupt:
    # Stop motorer og ryd op når programmet afbrydes
    pwm_front_left.stop()
    pwm_front_right.stop()
    pwm_back_left.stop()
    pwm_back_right.stop()
    GPIO.cleanup()
    print("Program stoppet og GPIO ryddet op.")

