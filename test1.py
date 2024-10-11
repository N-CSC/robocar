import RPi.GPIO as GPIO
import time
from sshkeyboard import listen_keyboard

# ... (rest of the code remains the same until the `try` block)

try:
    while True:
        # Listen for keyboard events
        key = listen_keyboard()

        # Handle the keyboard events
        if key == "w":
            set_individual_speeds(60, 60, 60, 60)  # forward
        elif key == "s":
            set_individual_speeds(-60, -60, -60, -60)  # backward
        elif key == "a":
            set_individual_speeds(0, 80, 0, 80)  # left
        elif key == "d":
            set_individual_speeds(80, 0, 80, 0)  # right
        elif key == "space":
            stop_motors()  # stop
        else:
            print("Invalid key")

        time.sleep(0.001)  # adjust the sleep time as needed

except KeyboardInterrupt:
    # Stop motorer og ryd op når programmet afbrydes
    pwm_front_left.stop()
    pwm_front_right.stop()
    pwm_back_left.stop()
    pwm_back_right.stop()
    GPIO.cleanup()
    print("Program stoppet og GPIO ryddet op.")
