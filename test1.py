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

GPIO.setup(SENSOR_LEFT, GPIO.IN)
GPIO.setup(SENSOR_RIGHT, GPIO.IN)

# Create PWM objects for speed control
pwm_front_left = GPIO.PWM(PWM1_Front, 100)  # 100Hz for front left motor
pwm_front_right = GPIO.PWM(PWM2_Front, 100)  # 100Hz for front right motor
pwm_back_left = GPIO.PWM(PWM1_Back, 100)  # 100Hz for back left motor
pwm_back_right = GPIO.PWM(PWM2_Back, 100)  # 100Hz for back right motor

# Start PWM med 0% duty cycle
pwm_front_left.start(0)
pwm_front_right.start(0)
pwm_back_left.start(0)
pwm_back_right.start(0)

# Debounce-funktion
def debounce_sensor(sensor_pin):
    stable_value = GPIO.input(sensor_pin)  # Læs den nuværende værdi
    time.sleep(0.5)  # Vent lidt
    return stable_value == GPIO.input(sensor_pin)  # Kontroller stabilitet

# Funktioner til motorstyring
def set_individual_speeds(front_left_speed, front_right_speed, back_left_speed, back_right_speed):
    # Juster hastigheder individuelt for hver motor og reducer med 10%
    pwm_front_left.ChangeDutyCycle(front_left_speed * 0.8)  # 80% af max hastighed
    pwm_front_right.ChangeDutyCycle(front_right_speed * 0.8)  # 80% af max hastighed
    pwm_back_left.ChangeDutyCycle(back_left_speed * 0.8)  # 80% af max hastighed
    pwm_back_right.ChangeDutyCycle(back_right_speed * 0.8)  # 80% af max hastighed

# Hovedprogram til at styre motorer baseret på sensorer
try:
    while True:
        # Læs sensorernes værdier med debounce
        left_value = debounce_sensor(left_sensor)  # 0 = ingen refleksion (hvid), 1 = refleksion (sort)
        right_value = debounce_sensor(right_sensor)

        # Udskriv sensorværdier til terminalen
        print(f"Venstre sensor: {left_value}, Højre sensor: {right_value}")

        # Motorstyring baseret på sensor-input
        if left_value == 0 and right_value == 0:
            # Begge sensorer ser hvidt -> Sænk hastigheden for alle hjul
            set_individual_speeds(60, 60, 60, 60)  # Sænk hastigheden på alle hjul
        elif left_value == 0 and right_value == 1:
            # Venstre sensor ser hvid -> Stop venstre forhjul og baghjul, højre kører hurtigere
            set_individual_speeds(0, 60, 0, 60)  # Stop venstre hjul, højre kører fuld kraft
        elif left_value == 1 and right_value == 0:
            # Højre sensor ser hvid -> Stop højre forhjul og baghjul, venstre kører hurtigere
            set_individual_speeds(60, 0, 60, 0)  # Stop højre hjul, venstre kører fuld kraft
        else:
            # Begge sensorer ser sort -> Kør fremad med fuld kraft
            set_individual_speeds(60, 60, 60, 60)  # Fuld hastighed på alle hjul

        time.sleep(0.001)  # Vent lidt før næste aflæsning

except KeyboardInterrupt:
    # Stop motorer og ryd op når programmet afbrydes
    pwm_front_left.stop()
    pwm_front_right.stop()
    pwm_back_left.stop()
    pwm_back_right.stop()
    GPIO.cleanup()
    print("Program stoppet og GPIO ryddet op.")
