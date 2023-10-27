print("init...")

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getchh = _Getch()

def SAO(fileName):
    try:
        os.system ( fileName)
    except Exception as error:
        global clear_screen
        clear_screen = False
        print("e -", error)
    

def SafeAsyncOpen(fileName):
    key = Thread( target= SAO(fileName))
    key.start()

def crash(x):
    # create and open crash.log
    fileName = "crash_log.txt"
    with open(fileName, 'w') as f:
        f.write(x + "\n\n\nCTRL + w   auto close notepad :)")
    # todo append new string, dont overwrite all
    SafeAsyncOpen(fileName)

import os
import sys
import yaml
import shutil
import ctypes

def UpdateConfig():
    # load that shit into mem
    try:
        with open("config.yml", 'r') as f:
            config = yaml.safe_load(f)
        # if config['keep_metadata'] == False:
        #     print("lkmfa")
        global compiler_name
        compiler_name = config["compiler_name"]

        global project_name
        project_name = config["project_name"]
        ctypes.windll.kernel32.SetConsoleTitleA(project_name)
        global project_extender
        project_extender = config["project_extender"]

        global with_build
        with_build = config["with_build"]

        global clear_screen
        clear_screen = config["clear_screen"]

    except Exception as error:
        print("e -", error)
        crash("config.yml not found!\ne -" + error)
        darby = getchh()
        exit()


#todo
UpdateConfig()

def ClearScreen():
    if (clear_screen == True):
        os.system('cls')

def getch():
    return getchh().decode("utf-8") 
    #depc, it cant visualize ESC 

def Dumpproducttodesktop():
    # destination = os.path.join(os.path.join(os.environ['USERPROFILE']), targetDir)
    destination = os.path.normpath(os.path.expanduser("~/" + targetDir))
    # source = os.getcwd() + "\product"
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)
    source = application_path + "\product"
    # config_path = os.path.join(application_path, config_name)
    # print(targetDir)

    allfiles = os.listdir(source)
    ress = 0
    for f in allfiles:
        ress = 1
        src_path = os.path.join(source, f)
        dst_path = os.path.join(destination, f)
        shutil.move(
            src_path,
            dst_path)
    
    return ress

def DumpProducts():
    x = 1
    try:
        x = Dumpproducttodesktop()
    except Exception as error:
        crash("warning -", error)
        print("\033[2;31;43m dumping error.! your "+ FormatCode(targetFormat)+" will be stored in product\033[0;0m")
        return 0
    
    return x # success

def SafeDumpAll():
    x = DumpProducts()
    if (x == 1):
        print("success - moved to C:/LOCALCLIENT/" + targetDir)
    else:
        crash("invalid URL")

def OpenConfig():
    SAO("config.yml")

def BuildOut():
    # x | <link> 
    # x = "nx_ref " + x
    print("....")

    if (with_build == "PATH"):
        print("using "+ with_build+ " from your path")
        
        x = compiler_name + " " + project_name + project_extender
        os.system(x)
        return 1
        
    else:
        print("using "+ with_build+ " from local dir ")
        pipIn = "\\" + with_build
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            application_path = os.path.dirname(__file__)
        source = application_path + pipIn
    source = source + "\\"+ project_name + ".exe"

    os.startfile(source)
    
    # x = compiler_name + " " + project_name + project_extender
    # os.system(x)
    return 1

def CarryOut():
    os.system(project_name + ".exe")
    return 1

def getresponse():
    ino = b'na'
    ress = 0 # ESC
    print("target: " + compiler_name + " "+ project_name + project_extender)
    while (ino != b'\x1b' ):
        print("[ESC -ext]\n[a - run latest ver]\n[b - build]\n[e - config]\n[u - update config.yml]: ")
        ino = getchh()
        print("bytecode", ino)
        
        #to opcode
        if (ino == b'a'):
            ress = 1
            break
        elif (ino == b'b'):
            ress = 2
            break
        elif (ino == b'e'):
            ress = 3
            break
        elif (ino == b'u'):
            ress = 4
            break
        
    ClearScreen()
    return ress

while (1): # core
    ress = getresponse()
    if (ress == 0):
        #exit
        exit()
    elif (ress == 1):
        # run latest version
        CarryOut()
    elif (ress == 2):
        # build latest version
        BuildOut()
        continue
    elif (ress == 3):
        OpenConfig()
    elif (ress == 4):
        print("updating config...")
        UpdateConfig()
    
    print("task finished - richard\n")
    # else continue