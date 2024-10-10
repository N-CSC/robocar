import RPi.GPIO as GPIO
import time

# Define the GPIO pin connected to the TCRT5000 OUT pin
TCRT_PIN = 4  # Change to the GPIO pin you connected the TCRT5000 to

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TCRT_PIN, GPIO.IN)

# Function to test the sensor
def test_sensor():
    try:
        while True:
            sensor_value = GPIO.input(TCRT_PIN)  # Read sensor value
            if sensor_value == 0:
                print("Object detected!")  # Output LOW when detecting an object (depends on wiring and configuration)
            else:
                print("No object detected")  # Output HIGH when no object is present
            time.sleep(0.5)  # Add a small delay to avoid spamming

    except KeyboardInterrupt:
        print("Exiting the test.")
    finally:
        GPIO.cleanup()  # Clean up GPIO on exit

# Run the sensor test
test_sensor()
