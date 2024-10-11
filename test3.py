from sshkeyboard import listen_keyboard

def GoForward():
    print("going forward")

def GoBackward():
    print("going backward")

def TurnLeft():
    print("turning left")

def TurnRight():
    print("turning right")

def Stop():
    print("stopping")

def press(key):
    if key == "w":
        GoForward()
    elif key == "s":
        GoBackward()
    elif key == "a":
        TurnLeft()
    elif key == "d":
        TurnRight()
    elif key == "space":
        Stop()

def release(key):
    if key == "w" or key == "s" or key == "a" or key == "d" or key == "space":
        Stop()

listen_keyboard(on_press=press, on_release=release)


     
