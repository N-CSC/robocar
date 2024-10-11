from sshkeyboard import listen_keyboard

def GoForward():
    print("going forward")

def press(key):
    if key == "w":
        GoForward()



while True:
    listen_keyboard(on_press = press)