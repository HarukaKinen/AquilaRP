from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from GUI import Ui_MainWindow as UIM

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UIM()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())