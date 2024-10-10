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
GPIO.setup(left_sensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Pulldown-modstand
GPIO.setup(right_sensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Pulldown-modstand

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
    pwm_back_left.ChangeDutyCycle(40)  # Halv hastighed
    pwm_back_right.ChangeDutyCycle(40)  # Halv hastighed
    pwm_front_left.ChangeDutyCycle(40)  # Halv hastighed
    pwm_front_right.ChangeDutyCycle(40)  # Halv hastighed

def stop_motors():
    # Stop alle motorer
    pwm_front_left.ChangeDutyCycle(0)
    pwm_front_right.ChangeDutyCycle(0)
    pwm_back_left.ChangeDutyCycle(0)
    pwm_back_right.ChangeDutyCycle(0)

def activate_motors():
    # Genaktiver motorer med standard hastighed
    move_forward()

# Hovedprogram til at styre motorer baseret på sensorer
try:
    left_sensor_timer = 0  # Tæller for venstre sensor
    right_sensor_timer = 0  # Tæller for højre sensor

    while True:
        # Læs sensorernes værdier
        left_value = GPIO.input(left_sensor)  # 0 = ingen refleksion (hvid tape), 1 = refleksion (sort)
        right_value = GPIO.input(right_sensor)

        # Udskriv sensorværdier til terminalen
        print(f"Venstre sensor: {left_value}, Højre sensor: {right_value}")

        # Håndter venstre sensor
        if left_value == 0:  # Sensor registrerer refleksion (hvidt)
            stop_motors()  # Stop motorerne
            left_sensor_timer = time.time()  # Nulstil timeren
        elif left_value == 1 and time.time() - left_sensor_timer >= 2:  # Sensor ikke registrerer refleksion
            activate_motors()  # Genaktiver motorer efter 2 sekunder

        # Håndter højre sensor
        if right_value == 0:  # Sensor registrerer refleksion (hvidt)
            stop_motors()  # Stop motorerne
            right_sensor_timer = time.time()  # Nulstil timeren
        elif right_value == 1 and time.time() - right_sensor_timer >= 2:  # Sensor ikke registrerer refleksion
            activate_motors()  # Genaktiver motorer efter 2 sekunder

        time.sleep(0.1)  # Vent lidt før næste aflæsning

except KeyboardInterrupt:
    # Stop motorer og ryd op når programmet afbrydes
    pwm_front_left.stop()
    pwm_front_right.stop()
    pwm_back_left.stop()
    pwm_back_right.stop()
    GPIO.cleanup()
    print("Program stoppet og GPIO ryddet op.")
