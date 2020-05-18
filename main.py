from pypresence import Presence
import pygetwindow as gw
import win32com.client
import requests
import time
import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread
from GUI import Ui_MainWindow as UIM

class NewUiMainWindow(UIM):
    def setupFunction(self):
        self.my_thread = MyThread()
        self.my_thread.start()
        self.enable_aqn.clicked.connect(self.ApplyAQNSetting)
        self.enable_fake.clicked.connect(self.ApplyFakeSetting)
        self.disable_aqn.clicked.connect(self.disable_rpc)
        self.disable_fake.clicked.connect(self.disable_rpc)

    def disable_rpc(self):
        pass

    def ApplyAQNSetting(self):
        pass

    def ApplyFakeSetting(self):
        pass

class MyThread(QThread):
    def __init__(self):
        super(MyThread, self).__init__()
        self.count = 0

    def run(self):
        while True:
            check_exsit("osu!.exe")
            time.sleep(3)


osu_close = False
gameOpend = False
state = any
current_active = any

client_id_osu = "367827983903490050"
RPC_osu = Presence(client_id_osu)
RPC_osu.connect()

client_id_aqn = "707510270771068945"
RPC_aqn = Presence(client_id_aqn)
RPC_aqn.connect()

def read_hosts():
    path = 'C:\Windows\System32\drivers\etc'
    os.chdir(path)
    file = 'hosts'
    with open(file, 'r') as fs:
        data = fs.readlines()
    return data

def getActive():
    global state
    global current_active
    tittle = gw.getActiveWindowTitle()
    keyword = "osu!"
    keyword_full = "osu!  - "
    if keyword in str(tittle):
        if keyword_full in str(tittle):
            if ".osu" in str(tittle):
                state = tittle.replace("osu!  - ", "").replace(".osu", "")
                currentactive = "edit"
            else:
                state = tittle.replace("osu!  - ", "")
                current_active = "play"
        else:
            state = "Idle"
        if state == "osu!":
            state = "Idle"
        elif "watching" in state:
            specname = tittle.replace("osu!  -  (watching ", "").replace(")", "")
            state = f"Spectating {specname}"
            current_active = "spectate"
    else:
        state = "AFK"
    return state, current_active

def check_server():
    datas = read_hosts()
    if "ppy.sh" in str(datas):
        if "163.172.255.98" in str(datas):
            server = "gatari"
        elif "159.65.235.81" in str(datas):
            server = "akatsuki"
        elif "88.198.32.213" in str(datas):
            server = "kawata"
        elif "51.15.26.118" in str(datas):
            server = "ripple"
        elif "194.34.133.95" in str(datas):
            server = "ainu"
        # elif "47.89.44.19" in str(datas):
        #     server = "ppy.sb"
        else:
            server = "unknown"
    else:
        server = "bancho"
    return server

def aqn_Active():
    state, current_active = getActive()
    server = check_server()
    if state == "AFK" or state == "Idle":
        RPC_aqn.update(details = state, large_image= "aqn", large_text="TheAquila Client", small_image = server, small_text = f"Playing on {server} server")
    else:
        if current_active == "play":
            active = "Getting good"
        elif current_active == "edit":
            active = "Resolving beatmap"
        elif current_active == "spectate":
            active = "Get good"
        RPC_aqn.update(details = state, state = active, large_image="aqn", large_text="TheAquila Cilent", small_image = server, small_text = f"Playing on {server} server")

def fake_setActive():
    state, current_active = getActive()
    if state == "AFK" or state == "Idle":
        RPC_osu.update(details = state, large_image= "osu_logo", large_text=f"username (rank #rank)", small_image = "mode_0", small_text = "osu")
    else:
        if current_active == "play":
            active = "Clicking circles"
            RPC_osu.update(details = state, large_image= "osu_logo", large_text=f"username (rank #rank)", small_image = "mode_0", small_text = "osu", spectate = "any")
        elif current_active == "edit":
            active = "Modding a Beatmap"
            RPC_osu.update(details = state, large_image= "osu_logo", large_text=f"username (rank #rank)", small_image = "mode_0", small_text = "osu")
        elif current_active == "spectate":
            active = "Spectating ?"
            RPC_osu.update(details = state, large_image= "osu_logo", large_text=f"username (rank #rank)", small_image = "mode_0", small_text = "osu")

def check_exsit(process_name):
    global osu_close
    global gameOpend
    WMI = win32com.client.GetObject('winmgmts:')
    processCodeCov = WMI.ExecQuery('select * from Win32_Process where Name="%s"' % process_name)
    if len(processCodeCov) > 0:
        osu_run = True
        if osu_run == True and osu_close == True and gameOpend != True:
            print("osu!.exe has been detected")
            osu_close = False
            gameOpend = True
    else:
        osu_run = False
        if osu_run != True and osu_close != True and gameOpend == True:
            print("osu!.exe closed")
            osu_close = True
            gameOpend = False
        elif osu_run != True and osu_close != True and gameOpend != True:
            print("osu!.exe cannot be detect")
            osu_close = True
            gameOpend = False
    return osu_run

def check_update():
    version = "1.0.1"
    try:
        r = requests.get('https://api.github.com/repos/Kotoki1337/AquilaRP/releases/latest')
        latest = r.json()["tag_name"]
        print(f"Version: {version}\nhttps://github.com/Kotoki1337/AquilaRP")
        if latest != version:
            print("There is a new release on Github!")
        else:
            print(f"The {version} is the latest release in Github!")
    except:
        print("Get release failed.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = NewUiMainWindow()
    ui.setupUi(MainWindow)
    ui.setupFunction()
    MainWindow.show()
    check_update()
    sys.exit(app.exec_())