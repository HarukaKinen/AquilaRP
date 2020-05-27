# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
import sys


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(359, 212)
        MainWindow.setWindowIcon(QIcon("AQN.ico"))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.formLayout = QtWidgets.QFormLayout(self.tab)
        self.formLayout.setObjectName("formLayout")
        self.server_enable = QtWidgets.QCheckBox(self.tab)
        self.server_enable.setObjectName("server_enable")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.server_enable)
        self.enable_aqn = QtWidgets.QPushButton(self.tab)
        self.enable_aqn.setObjectName("enable_aqn")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.enable_aqn)
        self.disable_aqn = QtWidgets.QPushButton(self.tab)
        self.disable_aqn.setObjectName("disable_aqn")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.disable_aqn)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout.setObjectName("gridLayout")
        self.username_label = QtWidgets.QLabel(self.tab_2)
        self.username_label.setObjectName("username_label")
        self.gridLayout.addWidget(self.username_label, 0, 0, 1, 1)
        self.mode_label = QtWidgets.QLabel(self.tab_2)
        self.mode_label.setObjectName("mode_label")
        self.gridLayout.addWidget(self.mode_label, 2, 0, 1, 1)
        self.rank_label = QtWidgets.QLabel(self.tab_2)
        self.rank_label.setObjectName("rank_label")
        self.gridLayout.addWidget(self.rank_label, 1, 0, 1, 1)
        self.rank_input = QtWidgets.QLineEdit(self.tab_2)
        self.rank_input.setObjectName("rank_input")
        self.gridLayout.addWidget(self.rank_input, 1, 1, 1, 1)
        self.username_input = QtWidgets.QLineEdit(self.tab_2)
        self.username_input.setObjectName("username_input")
        self.gridLayout.addWidget(self.username_input, 0, 1, 1, 1)
        self.enable_fake = QtWidgets.QPushButton(self.tab_2)
        self.enable_fake.setObjectName("enable_fake")
        self.gridLayout.addWidget(self.enable_fake, 3, 1, 1, 1)
        self.mod_combobox = QtWidgets.QComboBox(self.tab_2)
        self.mod_combobox.setEditable(False)
        self.mod_combobox.setObjectName("mod_combobox")
        self.mod_combobox.addItem("")
        self.mod_combobox.addItem("")
        self.mod_combobox.addItem("")
        self.mod_combobox.addItem("")
        self.gridLayout.addWidget(self.mod_combobox, 2, 1, 1, 1)
        self.disable_fake = QtWidgets.QPushButton(self.tab_2)
        self.disable_fake.setObjectName("disable_fake")
        self.gridLayout.addWidget(self.disable_fake, 4, 1, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.tab_3)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_2.addWidget(self.textBrowser, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Aquila Rich-Presence"))
        self.server_enable.setText(_translate("MainWindow", "Disable servers name"))
        self.enable_aqn.setText(_translate("MainWindow", "Start Presence"))
        self.disable_aqn.setText(_translate("MainWindow", "Stop Rich Presence"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Aquila"))
        self.username_label.setText(_translate("MainWindow", "Username"))
        self.mode_label.setText(_translate("MainWindow", "GameMode"))
        self.rank_label.setText(_translate("MainWindow", "Rank"))
        self.enable_fake.setText(_translate("MainWindow", "Start Presence"))
        self.mod_combobox.setCurrentText(_translate("MainWindow", "osu!"))
        self.mod_combobox.setItemText(0, _translate("MainWindow", "osu!"))
        self.mod_combobox.setItemText(1, _translate("MainWindow", "osu!taiko"))
        self.mod_combobox.setItemText(2, _translate("MainWindow", "osu!catch"))
        self.mod_combobox.setItemText(3, _translate("MainWindow", "osu!mania"))
        self.disable_fake.setText(_translate("MainWindow", "Stop Rich Presence"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Fake"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Log"))

    def outputWritten(self, text):
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()


class EmittingStr(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)
    def write(self, text):
        self.textWritten.emit(str(text))
