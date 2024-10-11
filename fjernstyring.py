from sshkeyboard import listen_keyboard
import RPi.GPIO as GPIO
import time
import socket

# ... (rest of the code remains the same until the `try` block)

try:
    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_address = ('', 8080)  # Use an available port
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    print("Waiting for connection...")

    # Accept an incoming connection
    connection, client_address = sock.accept()
    print(f"Connected to {client_address}")

    while True:
        # Receive data from the client (your computer)
        data = connection.recv(1024)

        # Parse the received data
        if data:
            command = data.decode().strip()
            print(f"Received command: {command}")

            # Handle the command
            if command == "forward":
                set_individual_speeds(60, 60, 60, 60)
            elif command == "backward":
                set_individual_speeds(-60, -60, -60, -60)
            elif command == "left":
                set_individual_speeds(0, 80, 0, 80)
            elif command == "right":
                set_individual_speeds(80, 0, 80, 0)
            elif command == "stop":
                stop_motors()
            else:
                print("Invalid command")

        time.sleep(0.001)  # adjust the sleep time as needed

except KeyboardInterrupt:
    # Stop motorer og ryd op når programmet afbrydes
    pwm_front_left.stop()
    pwm_front_right.stop()
    pwm_back_left.stop()
    pwm_back_right.stop()
    GPIO.cleanup()
    print("Program stoppet og GPIO ryddet op.")