import RPi.GPIO as GPIO
import time

# Definer GPIO pins for linjesensorerne
left_sensor = 20  # Venstre sensor
right_sensor = 16  # Højre sensor

# Definer GPIO pins for TB6612 motor driver (forreste hjul)
IN1_Front_Left = 17  # Forreste venstre motor retning
IN2_Front_Left = 27  # Forreste venstre motor retning
PWM_Front_Left = 12  # PWM til hastighedskontrol forreste venstre

IN3_Front_Right = 22  # Forreste højre motor retning
IN4_Front_Right = 23  # Forreste højre motor retning
PWM_Front_Right = 13  # PWM til hastighedskontrol forreste højre

# Definer GPIO pins for TB6612 motor driver (bageste hjul)
IN1_Back_Left = 5  # Bageste venstre motor retning
IN2_Back_Left = 6  # Bageste venstre motor retning
PWM_Back_Left = 18  # PWM til hastighedskontrol bageste venstre

IN3_Back_Right = 19  # Bageste højre motor retning
IN4_Back_Right = 26  # Bageste højre motor retning
PWM_Back_Right =

