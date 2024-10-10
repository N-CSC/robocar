import RPi.GPIO as GPIO
import time

# Definer GPIO pins for TB6612 H-broer (forreste hjul)
DIR1_Front = 22  # Retningskontrol forreste venstre motor
PWM1_Front = 6  # Hastighedskontrol forreste venstre motor

DIR2_Front = 0  # Retningskontrol forreste højre motor
PWM2_Front = 12  # Hastighedskontrol forreste højre motor

# Definer GPIO pins for TB6612 H-broer (bageste hjul)
DIR1_Back = 3  # Retningskontrol bageste venstre motor
PWM1_Back = 24  # Hastighedskontrol bageste venstre motor

DIR2_Back = 14  # Retningskontrol bageste højre motor
PWM2_Back = 10  # Hastighedskontrol bageste højre motor

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR1_Front, GPIO.OUT)
GPIO.setup(PWM1_Front, GPIO.OUT)
GPIO.setup(DIR2_Front, GPIO.OUT)
GPIO.setup(PWM2_Front, GPIO.OUT)

GPIO.setup(DIR1_Back, GPIO.OUT)
GPIO.setup(PWM1_Back, GPIO.OUT)
GPIO.setup(DIR2_Back, GPIO.OUT)
GPIO.setup(PWM2_Back, GPIO.OUT)

# Create PWM objects for speed control
pwm_front_left = GPIO.PWM(PWM1_Front, 100)  # 100Hz for front left motor
pwm_front_right = GPIO.PWM(PWM2_Front, 100)  # 100Hz for front right motor
pwm_back_left = GPIO.PWM(PWM1_Back, 100)  # 100Hz for back left motor
pwm_back_right = GPIO.PWM(PWM2_Back, 100)  # 100Hz for back right motor

# Start PWM with 50% duty cycle initially
pwm_front_left.start(50)
pwm_front_right.start(50)
pwm_back_left.start(50)
pwm_back_right.start(50)

# Function to move the vehicle forward
def move_forward():
    # Set direction to forward
    GPIO.output(DIR1_Front, True)
    GPIO.output(DIR2_Front, True)
    GPIO.output(DIR1_Back, True)
    GPIO.output(DIR2_Back, True)

# Function to move the vehicle backward
def move_backward():
    # Set direction to backward
    GPIO.output(DIR1_Front, False)
    GPIO.output(DIR2_Front, False)
    GPIO.output(DIR1_Back, False)
    GPIO.output(DIR2_Back, False)

# Function to stop all motors
def stop_motors():
    pwm_front_left.ChangeDutyCycle(0)
    pwm_front_right.ChangeDutyCycle(0)
    pwm_back_left.ChangeDutyCycle(0)
    pwm_back_right.ChangeDutyCycle(0)

# Function to set the speed for both left and right motors
def set_speed(left_speed, right_speed):
    # Adjust speed for left and right side motors
    pwm_front_left.ChangeDutyCycle(left_speed)
    pwm_front_right.ChangeDutyCycle(right_speed)
    pwm_back_left.ChangeDutyCycle(left_speed)
    pwm_back_right.ChangeDutyCycle(right_speed)

# Main loop to test forward and backward movement
try:
    while True:
        print("Moving forward")
        move_forward()
        set_speed(75, 75)  # Move forward with 75% speed
        time.sleep(5)      # Move for 5 seconds
        
        print("Moving backward")
        move_backward()
        set_speed(50, 50)  # Move backward with 50% speed
        time.sleep(5)      # Move for 5 seconds
        
        print("Stopping")
        stop_motors()      # Stop the motors
        time.sleep(2)      # Pause for 2 seconds

except KeyboardInterrupt:
    # Clean up the GPIO settings and stop PWM on interrupt
    pwm_front_left.stop()
    pwm_front_right.stop()
    pwm_back_left.stop()
    pwm_back_right.stop()
    GPIO.cleanup()
