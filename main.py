import time
import os

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

# Funktion til at eksportere og indstille GPIO
def setup_gpio(pin):
    # Eksportér pin og sæt den som output
    with open("/sys/class/gpio/export", "w") as f:
        f.write(str(pin))
    with open(f"/sys/class/gpio/gpio{pin}/direction", "w") as f:
        f.write("out")

# Funktion til at skrive værdi til en GPIO pin
def gpio_write(pin, value):
    with open(f"/sys/class/gpio/gpio{pin}/value", "w") as f:
        f.write(str(value))

# Initialiser GPIO pins
for pin in [left_sensor, right_sensor, DIR1_Front, PWM1_Front, DIR2_Front, PWM2_Front, DIR1_Back, PWM1_Back, DIR2_Back, PWM2_Back]:
    setup_gpio(pin)

def move_forward():
    gpio_write(DIR1_Front, 1)
    gpio_write(DIR2_Front, 1)
    gpio_write(DIR1_Back, 1)
    gpio_write(DIR2_Back, 1)

def turn_left():
    gpio_write(DIR1_Front, 1)
    gpio_write(DIR2_Front, 1)
    gpio_write(DIR1_Back, 1)
    gpio_write(DIR2_Back, 1)

def turn_right():
    gpio_write(DIR1_Front, 1)
    gpio_write(DIR2_Front, 1)
    gpio_write(DIR1_Back, 1)
    gpio_write(DIR2_Back, 1)

def stop_motors():
    gpio_write(DIR1_Front, 0)
    gpio_write(DIR2_Front, 0)
    gpio_write(DIR1_Back, 0)
    gpio_write(DIR2_Back, 0)

try:
    while True:
        # Læs sensorernes output
        left_detected = int(os.system(f"cat /sys/class/gpio/gpio{left_sensor}/value"))
        right_detected = int(os.system(f"cat /sys/class/gpio/gpio{right_sensor}/value"))
        
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
    for pin in [left_sensor, right_sensor, DIR1_Front, PWM1_Front, DIR2_Front, PWM2_Front, DIR1_Back, PWM1_Back, DIR2_Back, PWM2_Back]:
        with open("/sys/class/gpio/unexport", "w") as f:
            f.write(str(pin))
