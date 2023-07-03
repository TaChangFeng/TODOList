import sys
import main

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPalette, QPixmap, QBrush
from PyQt5.QtWidgets import QApplication, QMessageBox
from matplotlib.backends.backend_qt import MainWindow

#窗口UI设计
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1054, 757)
        # 设置背景图片
        palette = MainWindow.palette()
        brush = QBrush(QPixmap("pic2.jpg"))
        palette.setBrush(QPalette.Window, brush)

        MainWindow.setPalette(palette)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #欢迎语-文字标签
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(370, 80, 301, 121))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(43)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(260, 180, 501, 121))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(43)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        #开始使用-按钮
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(730, 360, 201, 71))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        #项目说明-按钮
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(730, 460, 201, 71))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        #退出程序-按钮
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(730, 560, 201, 71))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")

        #菜单栏
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1054, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        MainWindow.setMenuBar(self.menubar)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    #初始化组件及设置
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TODO列表工具"))
        self.label.setText(_translate("MainWindow", "欢迎使用"))
        self.label_2.setText(_translate("MainWindow", "TODO列表工具"))
        self.pushButton.setText(_translate("MainWindow", "开始使用"))
        self.pushButton_2.setText(_translate("MainWindow", "项目说明"))
        self.pushButton_3.setText(_translate("MainWindow", "退出程序"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.menu_2.setTitle(_translate("MainWindow", "菜单"))
        self.menu_3.setTitle(_translate("MainWindow", "说明"))
        self.menu_4.setTitle(_translate("MainWindow", "操作"))

        #按钮点击事件连接区
        self.pushButton_3.clicked.connect(MainWindow.confirm_exit)
        self.pushButton_2.clicked.connect(MainWindow.textwindow)
        self.pushButton.clicked.connect(self.open_new_window)

#功能函数类及窗口的加载
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

    #退出弹窗
    def confirm_exit(self):
        reply = QMessageBox.question(self, '退出程序', '确定要退出吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()
        else:
            pass

    #项目说明的文件读取
    def readfile(self):
        with open('Text2.txt', 'r',encoding='utf-8') as file:
            content = file.read()
        return content

    #项目说明弹窗
    def textwindow(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("项目说明")
        msgBox.setText(self.readfile())
        msgBox.addButton(QMessageBox.Ok)
        msgBox.exec_()

    #跳转下一个窗口，并关闭当前窗口
    def open_new_window(self):
        self.main_window2 = main.Ui_MainWindow2()
        self.main_window2.show()
        self.close()

#主窗口的加载初始化
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


