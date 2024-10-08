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
    # Juster hastigheder individuelt for hver motor
    pwm_front_left.ChangeDutyCycle(front_left_speed * 0.8)
    pwm_front_right.ChangeDutyCycle(front_right_speed * 0.8)
    pwm_back_left.ChangeDutyCycle(back_left_speed * 0.8)
    pwm_back_right.ChangeDutyCycle(back_right_speed * 0.8)

def stop_motors():
    # Stop alle motorer
    pwm_front_left.ChangeDutyCycle(0)
    pwm_front_right.ChangeDutyCycle(0)
    pwm_back_left.ChangeDutyCycle(0)
    pwm_back_right.ChangeDutyCycle(0)

# Hovedprogram til at styre motorer baseret på sensorer
try:
    while True:
        # Læs sensorernes værdier og inverter dem
        left_value = not GPIO.input(left_sensor)  # Inverter værdien: 1 = refleksion, 0 = ingen refleksion
        right_value = not GPIO.input(right_sensor)

        # Udskriv sensorværdier til terminalen
        print(f"Venstre sensor: {left_value}, Højre sensor: {right_value}")

        # Motorstyring baseret på sensor-input
        if left_value == 1 and right_value == 1:
            # Begge sensorer ser hvidt -> Sænk hastigheden for alle hjul
            set_individual_speeds(50, 50, 50, 50)  # Sænk hastigheden på alle hjul
        elif left_value == 1 and right_value == 0:
            # Venstre sensor ser hvid -> Sænk venstre forhjul og baghjul
            set_individual_speeds(10, 70, 10, 70)  # Venstre hjul sænkes, højre kører fuld kraft
        elif left_value == 0 and right_value == 1:
            # Højre sensor ser hvid -> Sænk højre forhjul og baghjul
            set_individual_speeds(70, 10, 70, 10)  # Højre hjul sænkes, venstre kører fuld kraft
        else:
            # Begge sensorer ser sort -> Kør fremad med fuld kraft
            set_individual_speeds(100, 100, 100, 100)  # Fuld hastighed på alle hjul

        time.sleep(0.1)  # Vent lidt før næste aflæsning

except KeyboardInterrupt:
    # Stop motorer og ryd op når programmet afbrydes
    pwm_front_left.stop()
    pwm_front_right.stop()
    pwm_back_left.stop()
    pwm_back_right.stop()
    GPIO.cleanup()
    print("Program stoppet og GPIO ryddet op.")
