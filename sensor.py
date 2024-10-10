import RPi.GPIO as GPIO
import time

# Definer GPIO pins for TCRT5000 sensorerne
left_sensor = 15  # GPIO pin til venstre sensor
right_sensor = 23  # GPIO pin til højre sensor

# Definer GPIO pins for TB6612 H-broer (motorer)
DIR1_Front = 22  # Retningskontrol forreste venstre motor
PWM1_Front = 6   # Hastighedskontrol forreste venstre motor
DIR2_Front = 0    # Retningskontrol forreste højre motor
PWM2_Front = 12   # Hastighedskontrol forreste højre motor
DIR1_Back = 3    # Retningskontrol bageste venstre motor
PWM1_Back = 24   # Hastighedskontrol bageste venstre motor
DIR2_Back = 14   # Retningskontrol bageste højre motor
PWM2_Back = 10    # Hastighedskontrol bageste højre motor

# Opsæt GPIO pins
GPIO.setmode(GPIO.BCM)

# Opsæt motor og sensor pins
motor_pins = [(DIR1_Front, PWM1_Front), (DIR2_Front, PWM2_Front), 
              (DIR1_Back, PWM1_Back), (DIR2_Back, PWM2_Back)]
for dir_pin, pwm_pin in motor_pins:
    GPIO.setup(dir_pin, GPIO.OUT)
    GPIO.setup(pwm_pin, GPIO.OUT)

# Opsæt sensor pins med pulldown-modstand
GPIO.setup(left_sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(right_sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Opret PWM objekter til hastighedskontrol
pwm_motors = [GPIO.PWM(pwm_pin, 100) for _, pwm_pin in motor_pins]
for pwm in pwm_motors:
    pwm.start(0)  # Start med 0% duty cycle

def set_motor_speed(left_speed, right_speed):
    # Juster hastighed for venstre og højre motorer
    pwm_motors[0].ChangeDutyCycle(left_speed)  # Venstre forreste
    pwm_motors[1].ChangeDutyCycle(right_speed)  # Højre forreste
    pwm_motors[2].ChangeDutyCycle(left_speed)  # Venstre bageste
    pwm_motors[3].ChangeDutyCycle(right_speed)  # Højre bageste

def move_forward():
    # Sæt retningen til fremad (ombyttet)
    GPIO.output(DIR1_Front, GPIO.LOW)   # Venstre motor fremad
    GPIO.output(DIR2_Front, GPIO.LOW)    # Højre motor fremad
    GPIO.output(DIR1_Back, GPIO.HIGH)    # Venstre bageste motor baglæns
    GPIO.output(DIR2_Back, GPIO.HIGH)     # Højre bageste motor baglæns
    set_motor_speed(100, 100)  # 100% hastighed
    print("Bevægelse: Fremad")

def move_backward():
    # Sæt retningen til baglæns (ombyttet)
    GPIO.output(DIR1_Front, GPIO.HIGH)   # Venstre motor baglæns
    GPIO.output(DIR2_Front, GPIO.HIGH)    # Højre motor baglæns
    GPIO.output(DIR1_Back, GPIO.LOW)      # Venstre bageste motor fremad
    GPIO.output(DIR2_Back, GPIO.LOW)       # Højre bageste motor fremad
    set_motor_speed(100, 100)  # 100% hastighed
    print("Bevægelse: Baglæns")

def turn_left():
    # Drej til venstre (ombyttet)
    GPIO.output(DIR1_Front, GPIO.LOW)  # Venstre motor fremad
    GPIO.output(DIR2_Front, GPIO.HIGH)  # Højre motor baglæns
    GPIO.output(DIR1_Back, GPIO.HIGH)   # Venstre bageste motor baglæns
    GPIO.output(DIR2_Back, GPIO.LOW)    # Højre bageste motor fremad
    set_motor_speed(100, 0)  # Venstre motor kører, højre motor stopper
    print("Dreje til venstre")

def turn_right():
    # Drej til højre (ombyttet)
    GPIO.output(DIR1_Front, GPIO.HIGH)  # Venstre motor baglæns
    GPIO.output(DIR2_Front, GPIO.LOW)   # Højre motor fremad
    GPIO.output(DIR1_Back, GPIO.LOW)    # Venstre bageste motor fremad
    GPIO.output(DIR2_Back, GPIO.HIGH)   # Højre bageste motor baglæns
    set_motor_speed(0, 100)  # Højre motor kører, venstre motor stopper
    print("Dreje til højre")

# Hovedprogram til at styre motorer baseret på sensorer
try:
    while True:
        left_value = GPIO.input(left_sensor)  # 0 = hvid, 1 = sort
        right_value = GPIO.input(right_sensor)

        # Udskriv sensorværdier
        print(f"Venstre sensor: {left_value}, Højre sensor: {right_value}")

        # Motorstyring baseret på sensor-input
        if left_value == 0 and right_value == 0:
            move_forward()
        elif left_value == 0 and right_value == 1:
            turn_right()
        elif left_value == 1 and right_value == 0:
            turn_left()
        else:
            set_motor_speed(0, 0)  # Stop motorerne direkte
            print("Motorer stoppet.")

        time.sleep(0.1)  # Vent lidt før næste aflæsning

except KeyboardInterrupt:
    set_motor_speed(0, 0)  # Stop motorerne
    for pwm in pwm_motors:
        pwm.stop()
    GPIO.cleanup()
    print("Program stoppet og GPIO ryddet op.")
