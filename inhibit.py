#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
import sys
import subprocess
import resources

class Inhibitation():
    def __init(self):
        self.__cookie = -1
        pass

    def start(self):
        self.__cookie = subprocess.Popen(["/usr/bin/qdbus", "org.freedesktop.PowerManagement", "/org/freedesktop/PowerManagement/Inhibit", "org.freedesktop.PowerManagement.Inhibit.Inhibit", "/usr/bin/plasmashell", "None"], stdout=subprocess.PIPE).communicate()[0]
        print(self.__cookie)

    def stop(self):
        print(subprocess.Popen(["/usr/bin/qdbus", "org.freedesktop.PowerManagement", "/org/freedesktop/PowerManagement/Inhibit", "org.freedesktop.PowerManagement.Inhibit.UnInhibit", self.__cookie], stdout=subprocess.PIPE).communicate()[0])

class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        self.__is_inhibited = False
        self.__inhibited_icon = QIcon(":/checked.img")
        self.__non_inhibited_icon = QIcon(":/not_checked.img")

        QSystemTrayIcon.__init__(self, parent=None)
        self.setIcon(self.__non_inhibited_icon)
        right_menu = RightClicked()
        self.setContextMenu(right_menu)
        self.setToolTip("Inhibit me ...")
        self.activated.connect(self.onActivation)
        self.inhibit = Inhibitation()

    def onActivation(self, activation_reason):
        if activation_reason == QSystemTrayIcon.Trigger:
            if self.__is_inhibited is True:
                self.__is_inhibited = False
                self.setIcon(self.__non_inhibited_icon)
                self.inhibit.stop()

            elif self.__is_inhibited is False:
                self.__is_inhibited = True
                self.setIcon(self.__inhibited_icon) 
                self.inhibit.start()

class RightClicked(QMenu):
    def __init__(self, parent=None):
        QMenu.__init__(self, parent=None)
        quit = QAction("Exit", self)
        quit.triggered.connect(lambda: QApplication.exit(0))

        # self.addSeparator()
        self.addAction(quit)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    tray_icon = TrayIcon()
    tray_icon.show()

    app.exec_()
