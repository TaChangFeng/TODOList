import os
import time
import pickle

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtCore import QFile, QIODevice, QMimeData, QTimer, QDateTime, QUrl
from PyQt5.QtGui import QPalette, QPixmap, QBrush
from io import StringIO

#事项类，对事项进行操作
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QLabel, QLineEdit, QDateTimeEdit, QVBoxLayout, \
    QFileDialog, QListWidgetItem, QListWidget, QPushButton, QHBoxLayout, QComboBox, QInputDialog, QDialog


class TodoItem:
    def __init__(self, text):
        self.text = text
        self.status = 'TODO'

    def __repr__(self):
        return f"【{self.status}】{self.text}"

class timewindow(QWidget):
    def __init__(self, parent = None, time_text = None ,text_edit = None):
        super(timewindow, self).__init__(parent)
        self.textEdit_20 = text_edit
        self.timewindow_text = time_text
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "设定提醒时间"))
        font5 = QtGui.QFont()
        font5.setFamily("微软雅黑")
        font5.setPointSize(12)
        self.setMinimumHeight(150)
        self.setFixedSize(500,500)
        self.label1 = QLabel("请设置本事项的提醒起止时间：")
        self.label1.setFont(font5)
        self.line_edit10 = QLineEdit(self)
        self.line_edit10.setReadOnly(True)
        self.line_edit10.setMinimumHeight(15)
        self.line_edit10.setMaximumHeight(50)
        self.line_edit10.setFont(font5)

        self.info_label = QLabel(self)


        self.label2 = QLabel("事项开始时间：")
        self.label2.setFont(font5)
        self.start_date_time_edit = QDateTimeEdit(self)
        self.start_date_time_edit.setMinimumHeight(15)
        self.start_date_time_edit.setMaximumHeight(50)
        self.start_date_time_edit.setFont(font5)
        self.label3 = QLabel("事项结束提醒时间：")
        self.label3.setFont(font5)
        self.end_date_time_edit = QDateTimeEdit(self)
        self.end_date_time_edit.setMinimumHeight(15)
        self.end_date_time_edit.setMaximumHeight(50)
        self.end_date_time_edit.setFont(font5)
        self.start_date_time_edit.setDateTime(QDateTime.currentDateTime())
        self.end_date_time_edit.setDateTime(QDateTime.currentDateTime())
        self.pushButton_20 = QtWidgets.QPushButton(self)
        self.pushButton_20.setGeometry(QtCore.QRect(930, 690, 121, 71))
        self.pushButton_20.setText(_translate("MainWindow", "保存时间"))
        self.pushButton_20.setFont(font5)
        self.pushButton_21 = QtWidgets.QPushButton(self)
        self.pushButton_21.setGeometry(QtCore.QRect(930, 690, 121, 71))
        self.pushButton_21.setText(_translate("MainWindow", "返回"))
        self.pushButton_21.setFont(font5)

        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.line_edit10)
        layout.addWidget(self.info_label)
        layout.addWidget(self.label2)
        layout.addWidget(self.start_date_time_edit)
        layout.addWidget(self.label3)
        layout.addWidget(self.end_date_time_edit)
        layout.addWidget(self.pushButton_20)
        layout.addWidget(self.pushButton_21)
        self.setLayout(layout)

        self.media_player = QMediaPlayer()

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_reminders)
        self.timer.start(1000)  # 每秒检查一次提醒

        self.reminders = []

        self.line_edit10.setText(self.timewindow_text)
        self.pushButton_20.clicked.connect(lambda: self.add_reminder(self.timewindow_text, self.start_date_time_edit.dateTime(), self.end_date_time_edit.dateTime()))
        self.pushButton_21.clicked.connect(self.close)

    def update_text_edit(self, text):
        self.textEdit_20.setPlainText(text)

    def add_reminder(self, item_text, start_datetime, end_datetime):
        reminder = {
            "item_text": item_text,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
            "status": "pending"
        }
        self.reminders.append(reminder)

    def check_reminders(self):
        current_datetime = QDateTime.currentDateTime()
        for reminder in self.reminders:
            if reminder["status"] == "pending" and current_datetime >= reminder["start_datetime"]:
                self.play_reminder_sound()
                self.info_label.setText(f"事项已开始: {reminder['item_text']}")
                reminder["status"] = "triggered"
                if self.textEdit_20 :
                    self.textEdit_20.append(f"【系统提示】 事项{reminder['item_text']}已开始")

            elif reminder["status"] == "triggered" and current_datetime >= reminder["end_datetime"]:
                self.play_reminder_sound()
                choice = self.show_end_reminder_dialog(reminder["item_text"])
                if choice == "结束":
                    print("【消息】选择结束")
                    reminder["status"] = "ended"
                    if self.textEdit_20:
                        self.textEdit_20.append(f"【系统提示】事项 {reminder['item_text']}已结束")
                elif choice == "推迟":
                    print("【消息】选择推迟")
                    minutes, ok = QInputDialog.getInt(self, '延迟', '延迟分钟数:', 1)
                    if ok:
                        reminder["start_datetime"] = reminder["start_datetime"].addSecs(minutes * 60)

    def show_end_reminder_dialog(self, item_text):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("事项结束")
        msg_box.setText(f"事项“{item_text} ”已结束！")
        end_button = msg_box.addButton("结束", QMessageBox.AcceptRole)
        postpone_button = msg_box.addButton("推迟", QMessageBox.RejectRole)
        msg_box.exec_()

        if msg_box.clickedButton() == end_button:
            return "结束"
        elif msg_box.clickedButton() == postpone_button:
            return "推迟"


    def play_reminder_sound(self):
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile("bgm.mp3")))
        self.media_player.play()
        print("【消息】音频已播放")

#窗口类
class Ui_MainWindow2(QtWidgets.QMainWindow):
    #初始化内容
    def __init__(self, parent=None):
        super(Ui_MainWindow2, self).__init__(parent)
        # 初始化数据
        default_file_name = "datafile.txt"
        file_path2 = os.path.join(os.getcwd(), default_file_name)
        try:
            # 打开文件
            with open(file_path2, 'rb') as file:
                self.items = pickle.load(file)
                print("【消息】写入文件成功，文件位于：", file_path2)
        except Exception as e:
            print("【消息】写入文件失败！位置38", file_path2)
            print("【消息】错误：", str(e))
            self.exportListToFile()
            self.items=[]
        self.item_dict={}
        self.setupUi2(self)

    #UI窗口设计
    def setupUi2(self, MainWindow2):
        self.setObjectName("MainWindow")
        MainWindow2.setFixedSize(1087, 836)
        QMessageBox.warning(self, "开始使用", "开始使用前，请详细阅读使用说明！", QMessageBox.Ok)
        # 设置背景图片
        palette = MainWindow2.palette()
        brush = QBrush(QPixmap("pic2.jpg"))
        palette.setBrush(QPalette.Window, brush)
        MainWindow2.setPalette(palette)

        self.centralwidget = QtWidgets.QWidget(MainWindow2)
        self.centralwidget.setObjectName("centralwidget")

        #我的事项-文字标签
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 40, 191, 51))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(27)
        self.label.setFont(font)
        self.label.setObjectName("label")

        #使用说明-按钮
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(800, 690, 121, 71))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setObjectName("pushButton_7")

        # 搜索-按钮
        self.pushButton_14 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_14.setGeometry(QtCore.QRect(680, 660, 81, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.pushButton_14.setFont(font)
        self.pushButton_14.setObjectName("pushButton")

        # 清除-按钮
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(580, 50, 181, 51))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setObjectName("pushButton_8")

        #字体样式设计
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)

        # 输入框
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(50, 660, 471, 41))
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(50, 600, 471, 41))
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(50, 540, 611, 41))
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setObjectName("lineEdit_3")

        # 修改-按钮
        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_9.setGeometry(QtCore.QRect(680, 600, 81, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setObjectName("pushButton_2")

        # 添加-按钮
        self.pushButton_10 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_10.setGeometry(QtCore.QRect(680, 540, 81, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.pushButton_10.setFont(font)
        self.pushButton_10.setObjectName("pushButton_3")

        # 下拉选择框
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(550, 600, 111, 41))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setFont(font)
        self.comboBox.addItems(['TODO', '正在进行', '已完成', '删除'])

        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(550, 660, 111, 41))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.setFont(font)
        self.comboBox_2.addItems(['全部','TODO', '正在进行', '已完成', '删除'])

        # 列表域
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(50, 110, 711, 411))
        font2 = QtGui.QFont()
        font2.setFamily("微软雅黑")
        font2.setPointSize(17)
        self.listWidget.setFont(font2)
        self.listWidget.setObjectName("listWidget")
        self.update_list()

        # 事项说明-文字标签
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(800, 390, 101, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        # 系统提示区-文字标签
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(800, 40, 131, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        # 文本域及输入框
        font20 = QtGui.QFont()
        font20.setFamily("微软雅黑")
        font20.setPointSize(10)
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(800, 80, 251, 301))
        self.textEdit_2.setFont(font20)
        self.textEdit_2.setReadOnly(True)
        self.textEdit_2.setObjectName("textEdit_2")
        #<main.Ui_MainWindow2 object at 0x000002AC0CEDEE50>
        self.time_window = timewindow(time_text="Your time text", text_edit=self.textEdit_2)
        self.time_window.update_text_edit("【系统提示】提示区运行正常")


        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(800, 430, 251, 241))
        self.textEdit.setFont(font2)
        self.textEdit.setObjectName("textEdit")

        # 设定-按钮
        self.pushButton_11 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_11.setGeometry(QtCore.QRect(550, 720, 211, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.pushButton_11.setFont(font)
        self.pushButton_11.setObjectName("pushButton_11")

        #退出程序-按钮
        self.pushButton_12 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_12.setGeometry(QtCore.QRect(930, 690, 121, 71))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.pushButton_12.setFont(font)
        self.pushButton_12.setObjectName("pushButton_12")

        #窗口基本信息
        MainWindow2.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow2)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1087, 26))
        self.menubar.setObjectName("menubar")
        MainWindow2.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow2)
        self.statusbar.setObjectName("statusbar")
        MainWindow2.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow2)

    #初始化UI
    def retranslateUi(self, MainWindow2):
        _translate = QtCore.QCoreApplication.translate
        MainWindow2.setWindowTitle(_translate("MainWindow", "TODO列表工具"))

        #组件加载区
        self.label.setText(_translate("MainWindow", "我的事项"))
        self.pushButton_7.setText(_translate("MainWindow", "使用说明"))
        self.pushButton_14.setText(_translate("MainWindow", "搜索"))
        self.pushButton_8.setText(_translate("MainWindow", "删除选中的事项"))
        self.pushButton_9.setText(_translate("MainWindow", "修改"))
        self.pushButton_10.setText(_translate("MainWindow", "添加"))
        self.label_2.setText(_translate("MainWindow", "事项说明"))
        self.label_3.setText(_translate("MainWindow", "系统提示区"))
        self.pushButton_11.setText(_translate("MainWindow", "为事项设定提醒时间"))
        self.pushButton_12.setText(_translate("MainWindow", "退出程序"))

        #按钮事件连接区
        self.pushButton_10.clicked.connect(self.add_item)
        self.listWidget.itemClicked.connect(self.show_item)
        self.pushButton_9.clicked.connect(self.edit_item)
        self.pushButton_12.clicked.connect(self.confirm_exit)
        #<main.Ui_MainWindow2 object at 0x0000021AE9D1DEE0>
        self.pushButton_11.clicked.connect(self.open_time_window)
        self.pushButton_14.clicked.connect(self.search)
        self.pushButton_7.clicked.connect(self.textwindow2)
        self.pushButton_8.clicked.connect(self.deleteItem)

    #添加事项
    def add_item(self):
        text = self.lineEdit_3.text()
        if text:
            item = TodoItem(text)
            self.items.append(item)
            self.update_list()
            self.lineEdit_3.clear()
            default_file_name = "datafile.txt"
            file_path2 = os.path.join(os.getcwd(), default_file_name)
            try:
                # 打开文件
                with open(file_path2, 'wb') as file:
                    pickle.dump(self.items,file)
                    print("【消息】写入文件成功，文件位于：", file_path2)
            except Exception as e:
                print("【消息】写入文件失败！位置258", file_path2)
                print("【消息】错误：", str(e))

    #获取事项说明
    def get_item(self):
        a=self.textEdit.toPlainText()
        return a

    #将结果反馈至列表
    def show_item(self, list_item):
        item_index = self.listWidget.indexFromItem(list_item).row()
        item = self.items[item_index]

        a=self.item_dict.get(item.text)
        self.lineEdit_2.setText(item.text)
        self.textEdit.setText(a)
        self.comboBox.setCurrentText(item.status)
        return item.text

    def gain_item(self):
        #获取文本框内容并显示到timewindow
        aa=self.lineEdit_2.text()
        return aa

    #对事项进行编辑（同时编辑事项标题和说明）
    def edit_item(self):
        item_index = self.listWidget.currentRow()
        item = self.items[item_index]
        item.text = self.lineEdit_2.text()
        a=self.get_item()
        self.item_dict[item.text]=a
        item.status = self.comboBox.currentText()
        self.update_list()

    #更新列表
    def update_list(self):
        self.listWidget.clear()
        for item in self.items:
            self.listWidget.addItem(str(item))
        self.exportListToFile()

    #退出弹窗
    def confirm_exit(self):
        reply = QMessageBox.question(self, '退出程序', '确定要退出吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()
        else:
            pass

    def open_time_window(self):
        m = self.gain_item()
        self.timew = timewindow(time_text=m,text_edit=self.textEdit_2)
        self.timew.show()

    #查找
    def search(self):
        search_text = self.lineEdit.text()
        choose = self.comboBox_2.currentText()
        searchlist = []
        for s in range(self.listWidget.count()):
            # 获取列表小部件中的项的文本
            item_text = self.listWidget.item(s).text()
            if search_text == "":
                if choose == '全部':
                    searchlist.extend([item_text])
                else:
                    for start in range(len(item_text)):
                        if item_text[start:start + len(choose)] == choose:
                            searchlist.extend([item_text])
            else:
                for start in range(len(item_text)):
                    if item_text[start:start + len(search_text)] == search_text:
                        if choose == "全部":
                            searchlist.extend([item_text])
                            break
            print(searchlist)
        self.searchs = searchwindow(search_text=searchlist)
        self.searchs.show()
        return searchlist

    def exportListToFile(self):
        # 设置默认文件路径和文件名
        default_file_name = "datafile.txt"
        file_path = os.path.join(os.getcwd(), default_file_name)
        try:
            # 打开文件
            with open(file_path, 'w', encoding='utf-8') as file:
                # 遍历列表小部件中的每一项
                for i in range(self.listWidget.count()):
                    # 获取列表小部件中的项的文本
                    item_text = self.listWidget.item(i).text()
                    # 将文本写入文件
                    file.write(item_text +"\n")
                print("写入文件成功，文件位于：", file_path)
        except Exception as e:
            print("写入文件失败！位置356", file_path)
            print("错误：", str(e))

    # 使用说明的文件读取
    def readfile2(self):
        with open('Text3.txt', 'r', encoding='utf-8') as file10:
            content2 = file10.read()
        return content2

    # 项目说明弹窗
    def textwindow2(self):
        msgBox2 = QMessageBox()
        msgBox2.setWindowTitle("项目说明")
        msgBox2.setText(self.readfile2())
        msgBox2.addButton(QMessageBox.Ok)
        msgBox2.exec_()

    def deleteItem(self):
        # 获取选中项的索引
        selectedIndexes = self.listWidget.selectedIndexes()
        # 遍历选中项的索引，从后往前删除
        for index in sorted(selectedIndexes, reverse=True):
            self.listWidget.takeItem(index.row())
            self.exportListToFile()

class searchwindow(QWidget):
    def __init__(self, parent=None, search_text=None):
        super(searchwindow, self).__init__(parent)
        self.searchlist = search_text
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "查找结果"))
        font5 = QtGui.QFont()
        font5.setFamily("微软雅黑")
        font5.setPointSize(12)
        self.setMinimumHeight(150)
        self.setFixedSize(500,150)
        self.label21 = QLabel("您的查找结果为：")
        self.label21.setFont(font5)
        self.listwidget20 = QListWidget(self)
        self.listwidget20.setMinimumHeight(15)
        self.listwidget20.setMaximumHeight(50)
        self.listwidget20.setFont(font5)
        self.pushButton_25 = QtWidgets.QPushButton(self)
        self.pushButton_25.setGeometry(QtCore.QRect(930, 690, 121, 71))
        self.pushButton_25.setText(_translate("MainWindow", "返回"))
        self.pushButton_25.setFont(font5)

        self.listwidget20.setGeometry(QtCore.QRect(50, 110, 711, 411))
        layout = QVBoxLayout()
        layout.addWidget(self.label21)
        layout.addWidget(self.listwidget20, stretch=1)
        layout.addWidget(self.pushButton_25)
        self.setLayout(layout)
        for sl in self.searchlist:
            QListWidgetItem(sl, self.listwidget20)
        self.pushButton_25.clicked.connect(self.close)


