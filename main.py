import RPi.GPIO as GPIO
import time

# Definer GPIO pins for linjesensorerne
left_sensor = 20  # GPIO til venstre TCRT5000 sensor
right_sensor = 16  # GPIO til højre TCRT5000 sensor

# Definer GPIO pins for forreste hjul (motor 1 og 2, H-bro 1)
DIR1_Front = 17  # Retningskontrol for venstre forreste motor
PWM1_Front = 12  # Hastighedskontrol for venstre forreste motor
DIR2_Front = 27  # Retningskontrol for højre forreste motor
PWM2_Front = 13  # Hastighedskontrol for højre forreste motor

# Definer GPIO pins for bageste hjul (motor 3 og 4, H-bro 2)
DIR1_Back = 5  # Retningskontrol for venstre bageste motor
PWM1_Back = 18  # Hastighedskontrol for venstre bageste motor
DIR2_Back = 6  # Retningskontrol for højre bageste motor
PWM2_Back = 19  # Hastighedskontrol for højre bageste motor

# Opsæt GPIO
GPIO.setmode(GPIO.BCM)

# Opsæt sensor GPIO som input
GPIO.setup(left_sensor, GPIO.IN)
GPIO.setup(right_sensor, GPIO.IN)

# Opsæt GPIO pins for forreste hjul
GPIO.setup(DIR1_Front, GPIO.OUT)
GPIO.setup(PWM1_Front, GPIO.OUT)
GPIO.setup(DIR2_Front, GPIO.OUT)
GPIO.setup(PWM2_Front, GPIO.OUT)

# Opsæt GPIO pins for bageste hjul
GPIO.setup(DIR1_Back, GPIO.OUT)
GPIO.setup(PWM1_Back, GPIO.OUT)
GPIO.setup(DIR2_Back, GPIO.OUT)
GPIO.setup(PWM2_Back, GPIO.OUT)

# Opret PWM objekter til hastighedskontrol (100 Hz frekvens)
pwm_front_left = GPIO.PWM(PWM1_Front, 100)  # Venstre forreste motor
pwm_front_right = GPIO.PWM(PWM2_Front, 100)  # Højre forreste motor
pwm_back_left = GPIO.PWM(PWM1_Back, 100)  # Venstre bageste motor
pwm_back_right = GPIO.PWM(PWM2_Back, 100)  # Højre bageste motor

# Start PWM med 0% duty cycle (motorerne er stoppet til at starte med)
pwm_front_left.start(0)
pwm_front_right.start(0)
pwm_back_left.start(0)
pwm_back_right.start(0)

def move_forward():
    # Sæt alle motorer til fremad
    GPIO.output(DIR1_Front, True)
    GPIO.output(DIR2_Front, True)
    GPIO.output(DIR1_Back, True)
    GPIO.output(DIR2_Back, True)
    
    # Sæt hastigheden til 50% for både forreste og bageste motorer
    pwm_front_left.ChangeDutyCycle(50)
    pwm_front_right.ChangeDutyCycle(50)
    pwm_back_left.ChangeDutyCycle(50)
    pwm_back_right.ChangeDutyCycle(50)

def turn_left():
    # Sæt retning til fremad, men drej til venstre (højre motor hurtigere)
    GPIO.output(DIR1_Front, True)
    GPIO.output(DIR2_Front, True)
    GPIO.output(DIR1_Back, True)
    GPIO.output(DIR2_Back, True)
    
    # Juster hastigheden: venstre motorer langsommere, højre hurtigere
    pwm_front_left.ChangeDutyCycle(25)  # 25% hastighed venstre forreste
    pwm_front_right.ChangeDutyCycle(50)  # 50% hastighed højre forreste
    pwm_back_left.ChangeDutyCycle(25)  # 25% hastighed venstre bageste
    pwm_back_right.ChangeDutyCycle(50)  # 50% hastighed højre bageste

def turn_right():
    # Sæt retning til fremad, men drej til højre (venstre motor hurtigere)
    GPIO.output(DIR1_Front, True)
    GPIO.output(DIR2_Front, True)
    GPIO.output(DIR1_Back, True)
    GPIO.output(DIR2_Back, True)
    
    # Juster hastigheden: højre motorer langsommere, venstre hurtigere
    pwm_front_left.ChangeDutyCycle(50)  # 50% hastighed venstre forreste
    pwm_front_right.ChangeDutyCycle(25)  # 25% hastighed højre forreste
    pwm_back_left.ChangeDutyCycle(50)  # 50% hastighed venstre bageste
    pwm_back_right.ChangeDutyCycle(25)  # 25% hastighed højre bageste

def stop_motors():
    # Stop alle motorer ved at sætte PWM duty cycle til 0
    pwm_front_left.ChangeDutyCycle(0)
    pwm_front_right.ChangeDutyCycle(0)
    pwm_back_left.ChangeDutyCycle(0)
    pwm_back_right.ChangeDutyCycle(0)

try:
    while True:
        # Læs sensorernes output
        left_detected = GPIO.input(left_sensor)  # Læs venstre sensor
        right_detected = GPIO.input(right_sensor)  # Læs højre sensor
        
        if left_detected == 0 and right_detected == 0:  # Begge sensorer på mørk baggrund
            move_forward()  # Kør ligeud
        elif left_detected == 1 and right_detected == 0:  # Venstre sensor på hvid tape
            turn_right()  # Drej til højre
        elif left_detected == 0 and right_detected == 1:  # Højre sensor på hvid tape
            turn_left()  # Drej til venstre
        else:
            stop_motors()  # Hvis begge sensorer er på hvid tape, stop

        time.sleep(0.1)  # Lille forsinkelse for stabil aflæsning

except KeyboardInterrupt:
    stop_motors()  # Stop motorerne ved afbrydelse
    GPIO.cleanup()  # Ryd op i GPIO-indstillingerne
