import RPi.GPIO as GPIO
import time

# Definer GPIO pins for TCRT5000 sensorerne
left_sensor = 4  # GPIO pin til venstre sensor
right_sensor = 16  # GPIO pin til højre sensor

# Opsæt GPIO pins som input med pull-down modstand
GPIO.setmode(GPIO.BCM)
GPIO.setup(left_sensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(right_sensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)


try:
    while True:
        # Læs sensorernes værdier
        left_value = GPIO.input(left_sensor)  # 0 = ingen refleksion (sort), 1 = refleksion (hvid tape)
        right_value = GPIO.input(right_sensor)

        # Udskriv værdierne til terminalen
        print(f"Venstre sensor: {left_value}, Højre sensor: {right_value}")
        
        # Vent 100 ms før næste aflæsning
        time.sleep(1)

except KeyboardInterrupt:
    # Ryd op når programmet afbrydes med Ctrl+C
    GPIO.cleanup()
    print("Program stoppet og GPIO ryddet op.")
