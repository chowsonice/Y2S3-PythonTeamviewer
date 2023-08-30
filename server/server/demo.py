
def baseRegistryKey(link):
    a = None
    if "\\" in link:
        key = link.split("\\")[0].upper()
        if key == "HKEY_CLASSES_ROOT":
            a = reg.HKEY_CLASSES_ROOT
        elif key == "HKEY_CURRENT_USER":
            a = reg.HKEY_CURRENT_USER
        elif key == "HKEY_LOCAL_MACHINE":
            a = reg.HKEY_LOCAL_MACHINE
        elif key == "HKEY_USERS":
            a = reg.HKEY_USERS
        elif key == "HKEY_CURRENT_CONFIG":
            a = reg.HKEY_CURRENT_CONFIG
    return a

def getvalue(a, link, valueName):
    try:
        a = reg.OpenKey(a, link)
    except Exception as ex:
        return "Lỗi"
    
    if a is None:
        return "Lỗi"
    
    try:
        op, type_ = reg.QueryValueEx(a, valueName)
    except Exception as ex:
        return "Lỗi"
    
    s = ""
    if type_ == reg.REG_MULTI_SZ:
        s = " ".join(op)
    elif type_ == reg.REG_BINARY:
        s = " ".join(str(byte) for byte in op)
    else:
        s = str(op)
    
    return s

def setvalue(a, link, valueName, value, typeValue):
    try:
        a = reg.OpenKey(a, link, 0, reg.KEY_SET_VALUE)
    except Exception as ex:
        return "Lỗi"
    
    if a is None:
        return "Lỗi"
    
    kind = None
    if typeValue == "String":
        kind = reg.REG_SZ
    elif typeValue == "Binary":
        kind = reg.REG_BINARY
    elif typeValue == "DWORD":
        kind = reg.REG_DWORD
    elif typeValue == "QWORD":
        kind = reg.REG_QWORD
    elif typeValue == "Multi-String":
        kind = reg.REG_MULTI_SZ
    elif typeValue == "Expandable String":
        kind = reg.REG_EXPAND_SZ
    else:
        return "Lỗi"
    
    try:
        if kind == reg.REG_DWORD:
            value = int(value)
        elif kind == reg.REG_QWORD:
            value = int(value)
        elif kind == reg.REG_MULTI_SZ:
            value = value.split()
        reg.SetValueEx(a, valueName, 0, kind, value)
    except Exception as ex:
        return "Lỗi"
    
    return "Set value thành công"

def deletevalue(a, link, valueName):
    try:
        a = reg.OpenKey(a, link, 0, reg.KEY_SET_VALUE)
    except Exception as ex:
        return "Lỗi"
    
    if a is None:
        return "Lỗi"
    
    try:
        reg.DeleteValue(a, valueName)
    except Exception as ex:
        return "Lỗi"
    
    return "Xóa value thành công"

def deletekey(a, link):
    try:
        reg.DeleteKey(a, link)
    except Exception as ex:
        return "Lỗi"
    
    return "Xóa key thành công"

def registry():
    while True:
        s = receiveSignal()  # Implement your receiveSignal() function
        
        if s == "REG":
            data = receiveData()  # Implement your receiveData() function
            
            with open("fileReg.reg", "w") as file:
                file.write(data)
            
            file_path = os.path.join(os.getcwd(), "fileReg.reg")
            test = True
            try:
                subprocess.run(["regedit.exe", "/s", file_path], check=True)
            except Exception as ex:
                test = False
            
            if test:
                nw.write("Sửa thành công")
            else:
                nw.write("Sửa thất bại")
            nw.flush()
        
        elif s == "QUIT":
            return
        
        elif s == "SEND":
            option = Program.nr.readline().strip()
            link = Program.nr.readline().strip()
            valueName = Program.nr.readline().strip()
            value = Program.nr.readline().strip()
            typeValue = Program.nr.readline().strip()
            
            a = baseRegistryKey(link)
            link2 = link.split("\\", 1)[1]
            
            if a is None:
                s = "Lỗi"
            else:
                if option == "Create key":
                    a = reg.CreateKey(a, link2)
                    s = "Tạo key thành công"
                elif option == "Delete key":
                    s = deletekey(a, link2)
                elif option == "Get value":
                    s = getvalue(a, link2, valueName)
                elif option == "Set value":
                    s = setvalue(a, link2, valueName)
                    s = setvalue(a, link2, valueName, value, typeValue)
                elif option == "Delete value":
                    s = deletevalue(a, link2, valueName)
                else:
                    s = "Lỗi"
            
            nw.write(s)
            nw.flush()