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
    pwm_front_left.ChangeDutyCycle(front_left_speed * 0.8)  # 90% af max hastighed
    pwm_front_right.ChangeDutyCycle(front_right_speed * 0.8)  # 90% af max hastighed
    pwm_back_left.ChangeDutyCycle(back_left_speed * 0.8)  # 90% af max hastighed
    pwm_back_right.ChangeDutyCycle(back_right_speed * 0.8)  # 90% af max hastighed

def stop_motors():
    # Stop alle motorer
    pwm_front_left.ChangeDutyCycle(0)
    pwm_front_right.ChangeDutyCycle(0)
    pwm_back_left.ChangeDutyCycle(0)
    pwm_back_right.ChangeDutyCycle(0)

# Hovedprogram til at styre motorer baseret på sensorer
try:
    
    while True:
        # Læs sensorernes værdier
        left_value = GPIO.input(left_sensor)  # 0 = ingen refleksion (hvid), 1 = refleksion (sort)
        right_value = GPIO.input(right_sensor)

        # Udskriv sensorværdier til terminalen
        print(f"Venstre sensor: {left_value}, Højre sensor: {right_value}")

        if left_value == 0 and right_value == 0:
            set_individual_speeds(60, 60, 60, 60)  
        elif left_value == 0 and right_value == 1:
            set_individual_speeds(0, 80, 0, 80) 
        elif left_value == 1 and right_value == 0:
            set_individual_speeds(80, 0, 80, 0)  
        else:
            set_individual_speeds(60, 60, 60, 60) 

        time.sleep(0.001)  # adjust the sleep time as needed

except KeyboardInterrupt:
    # Stop motorer og ryd op når programmet afbrydes
    pwm_front_left.stop()
    pwm_front_right.stop()
    pwm_back_left.stop()
    pwm_back_right.stop()
    GPIO.cleanup()
    print("Program stoppet og GPIO ryddet op.")
