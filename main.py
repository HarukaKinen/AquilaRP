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
        self.Checktimer, self.Faketimer = QTimer(), QTimer()
        self.Checktimer.timeout.connect(self.check_osu)
        self.Checktimer.start(1000)

        self.Faketimer.timeout.connect(self.ApplyFakeSetting)

        self.enable_fake.clicked.connect(lambda: self.Faketimer.start(1000))
        self.disable_fake.clicked.connect(self.stopRPC)

    def stopRPC(self):
        self.Faketimer.stop()
        RPC_osu.clear()

    def check_osu(self):  # aka Debug place
        check_exsit("osu!.exe")

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

def parse_int(num):
    to_str=str(num) #转换成字符串
    count=0 #循环计数
    sumstr='' #待拼接的字符串
    for one_str in to_str[::-1]: #注意循环是倒着输出的
        count += 1 #计数
        if count %3==0 and count != len(to_str): #如果count等于3或3的倍数并且不等于总长度
            one_str = ',' + one_str # 当前循环的字符串前面加逗号
            sumstr = one_str + sumstr #拼接当前字符串
        else:
            sumstr = one_str + sumstr #正常拼接字符串
    return sumstr #返回拼接的字符串

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
    keyword_beta = "osu!beta"
    keyword_cedge = "osu!cuttingedge b"
    keyword_full = "osu!  - "
    keyword_beta_full = "osu!beta  - "
    keyword_cedge_full = " - "
    if keyword in str(tittle):
        if keyword_beta in str(tittle):
            client_version = "beta"
        elif keyword_cedge in str(tittle):
            client_version = "cedge"
        else:
            client_version = "stb"
    else:
        client_version = "not osu"
    print(client_version)
    if client_version == "stb" or client_version == "beta":
        if keyword_full in str(tittle) or keyword_beta_full in str(tittle):
            if ".osu" in str(tittle):
                state = tittle.split('  - ', 1)[-1].replace(".osu", "")
                current_active = "edit"
            else:
                state = tittle.split('  - ', 1)[-1]
                current_active = "play"
        else:
            state = "Idle"
        if state == "osu!" or state == "osu!beta":
            state = "Idle"
        elif "(watching" in state:
            specname = tittle.split('  -  ', 1)[-1].replace("(watching ", "").replace(")", "")
            state = f"Spectating {specname}"
            current_active = "spectate"
    elif client_version == "cedge":
        if keyword_cedge in str(tittle) and keyword_cedge_full in str(tittle):
            if ".osu" in str(tittle):
                state = tittle.split(' - ', 1)[-1].replace(".osu", "")
                current_active = "edit"
            else:
                state = tittle.split(' - ', 1)[-1]
                current_active = "play"
        else:
            state = "Idle"
        if state == "osu!" or state == "osu!beta":
            state = "Idle"
        elif "(watching" in state:
            specname = tittle.split(' -  ', 1)[-1].replace("(watching ", "").replace(")", "")
            state = f"Spectating {specname}"
            current_active = "spectate"
    else:
        state = "AFK"
    return state, current_active

def fake_Active():
    state, current_active = getActive()
    osu_run = check_exsit("osu!.exe")
    mode = str(ui.mod_combobox.currentText())

    if ui.username_input.text() != "":
        username = ui.username_input.text()
        if ui.rank_input.text() !="":
            rank = ui.rank_input.text()
            if "," not in rank:
                rank = parse_int(rank)
            else:
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
                RPC_osu.update(details = "Idle", large_image = "osu_logo", large_text = userinfo, small_image = f"mode_{mode_int}", small_text = mode)
            elif current_active == "spectate":
                RPC_osu.update(details = "Idle", large_image = "osu_logo", large_text = userinfo, small_image = f"mode_{mode_int}", small_text = mode)
    else:
        RPC_osu.clear()

def check_exsit(process_name):
    global osu_close
    global gameOpend
    WMI = win32com.client.GetObject('winmgmts:')
    processCodeCov = WMI.ExecQuery('select * from Win32_Process where Name="%s"' % process_name)
    if len(processCodeCov) > 0:
        print("osu!.exe has been detected")
        osu_run = True
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
    version = "2.0.0-MPGH-Release"
    Author = "UID-5514764"
    print(f"Version: {version} by {Author}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui.setupUi(MainWindow)
    ui.setupFunction()
    MainWindow.show()
    check_update()
    sys.exit(app.exec_())