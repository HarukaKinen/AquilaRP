from pypresence import Presence
import pygetwindow as gw
import win32com.client
import requests
import time
import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from GUI import Ui_MainWindow as UIM


class NewUiMainWindow(UIM):
    def setupFunction(self):
        self.Checktimer, self.AQNtimer, self.Faketimer = QTimer(), QTimer(), QTimer()
        self.Checktimer.timeout.connect(self.check_osu)
        self.Checktimer.start(1000)

        self.AQNtimer.timeout.connect(self.ApplyAQNSetting)
        self.Faketimer.timeout.connect(self.ApplyFakeSetting)

        self.enable_aqn.clicked.connect(lambda: self.AQNtimer.start(1000))
        self.enable_fake.clicked.connect(lambda: self.Faketimer.start(1000))
        self.disable_aqn.clicked.connect(self.stopRPC)
        self.disable_fake.clicked.connect(self.stopRPC)

    def stopRPC(self):
        self.AQNtimer.stop()
        self.Faketimer.stop()
        RPC_aqn.clear()
        RPC_osu.clear()

    def check_osu(self):  # aka Debug place
        check_exsit("osu!.exe")

    def ApplyAQNSetting(self):
        aqn_Active()

    def ApplyFakeSetting(self):
        fake_Active()


ui = NewUiMainWindow()

state = any
current_active = any
osu_close = False
gameOpend = False

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
                current_active = "edit"
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
    osu_run = check_exsit("osu!.exe")
    state, current_active = getActive()
    if ui.server_enable.isChecked():  # enable写反了 呵呵
        server_disable = True
        print(ui.server_enable.isChecked())
        print("1")
    else:
        print(ui.server_enable.isChecked())
        print("0")
        server_disable = False
    if server_disable:
        server_name = None
        server = None
    else:
        server_name = check_server()
        print(server_name)
        server = f"Playing on {server_name} server"
    if osu_run:
        if state == "AFK" or state == "Idle":
            RPC_aqn.update(details = state, large_image = "aqn", large_text = "TheAquila Client", small_image = server_name, small_text = server)
        else:
            if current_active == "play":
                active = "Getting good"
            elif current_active == "edit":
                active = "Resolving beatmap"
            elif current_active == "spectate":
                active = "Get good"
            RPC_aqn.update(details = state, state = active, large_image = "aqn", large_text = "TheAquila Cilent", small_image = server_name, small_text = server)
    else:
        RPC_aqn.clear()


def fake_Active():
    state, current_active = getActive()
    osu_run = check_exsit("osu!.exe")
    mode = str(ui.mod_combobox.currentText())

    if ui.username_input.text() != "":
        username = ui.username_input.text()
        if ui.rank_input.text() !="":
            rank = ui.rank_input.text()
            userinfo = f"{username} (rank #{rank})"
        else:
            userinfo = f"{username}"
    else:
        userinfo = None

    if mode == "osu!":
        mode_int = "0"
        mode_active = "Clicking circles"
    if mode == "osu!taiko":
        mode_int = "1"
        mode_active = "Bashing drums"
    if mode == "osu!catch":
        mode_int = "2"
        mode_active = "Catching fruit"
    if mode == "osu!mania":
        mode_int = "3"
        mode_active = "Smashing keys"

    if osu_run:
        if state == "AFK" or state == "Idle":
            RPC_osu.update(details = state, large_image = "osu_logo", large_text = userinfo, small_image = f"mode_{mode_int}", small_text = mode)
        else:
            if current_active == "play":
                RPC_osu.update(details = state, state = mode_active, large_image = "osu_logo", large_text = userinfo, small_image = f"mode_{mode_int}", small_text = mode, spectate = "any")
            elif current_active == "edit":
                active = "Modding a Beatmap"
                RPC_osu.update(details = state, state = active, large_image = "osu_logo", large_text = userinfo, small_image = f"mode_{mode_int}", small_text = mode)
            elif current_active == "spectate":
                RPC_osu.update(details = "Idle", large_image = "osu_logo", large_text = userinfo, small_image = f"mode_{mode_int}", small_text = mode)
    else:
        RPC_osu.clear()
        RPC_aqn.clear()


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
        RPC_aqn.clear()
        RPC_osu.clear()
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
        print("Get latest release failed.")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui.setupUi(MainWindow)
    ui.setupFunction()
    MainWindow.show()
    check_update()
    sys.exit(app.exec_())