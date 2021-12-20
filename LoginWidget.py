import sys
import registerWidget
import mainWindowWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pymysql
import json


class TsLogin(QWidget):
    def __init__(self):
        super(TsLogin, self).__init__()
        self.initUI()
        self.mainWidget = mainWindowWidget.MainWindowWidget()

    def initUI(self):
        self.resize(600, 300)
        self.setWindowTitle("登陆界面")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.userLineEdit = QLineEdit()
        self.passwdLineEdit = QLineEdit()
        self.passwdLineEdit.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.loginBtn = QPushButton("登录")
        self.registerBtn = QPushButton("注册")
        self.exitBtn = QPushButton("退出")
        self.titleLabel = QLabel("图书管理系统")
        self.titleLabel.setFont(QFont("宋体", 20))
        self.titleLabel.setAlignment(Qt.AlignHCenter)
        self.exitBtn.clicked.connect(self.on_exit)
        self.registerBtn.clicked.connect(self.on_register)
        self.loginBtn.clicked.connect(self.on_login)

        layout = QGridLayout()

        layout.addWidget(self.titleLabel, 0, 0, 1, 3)
        layout.addWidget(QLabel("账户名："))

        layout.addWidget(self.userLineEdit, 1, 1, 1, 2)
        layout.addWidget(QLabel("密码："))

        layout.addWidget(self.passwdLineEdit, 2, 1, 1, 2)
        layout.addWidget(self.loginBtn, 3, 0, 1, 1)
        layout.addWidget(self.registerBtn, 3, 2, 1, 1)
        # layout.addWidget(self.exitBtn, 3, 2, 1, 1)
        # layout.addRow("账户名：",self.userLineEdit)
        # layout.addRow("密码：",self.passwdLineEdit)
        #
        # layout.addRow(QLabel(self))
        # layout.addRow(self.loginBtn,self.registerBtn)
        self.setLayout(layout)
        self.register = registerWidget.RegistryWidget()

        # self.registerBtn.clicked.connect(self.on_register)
        # self.loginBtn.clicked.connect(self.on_login)

    def on_login(self):
        con = pymysql.connect(host='172.28.22.15', user="root", port=53306, password="123456", database="tsglxt")
        su = con.cursor()
        sql = "SELECT * FROM users where id='{}' and passward='{}'".format(self.userLineEdit.text(),
                                                                                self.passwdLineEdit.text())
        print(sql)
        try:
            res = su.execute(sql)

            print(res)
            if res != 0:
                self.mainWidget.show()
                self.close()
                # 登录成功
                pass
            else:
                QMessageBox.information(self, "错误", "用户名或密码错误，请重新输入！", QMessageBox.Ok)
        except Exception as e:
            QMessageBox.critical(self, "错误！", e, QMessageBox.Ok)
        finally:


            print("登录")
        pass

    def on_register(self):
        self.register.registerStatus.connect(self.registerfun)
        self.register.show()

        print("注册")
        pass

    # 执行注册功能的函数
    def registerfun(self, data: dict):

        try:
            con = pymysql.connect(host='172.28.22.15', user="root", port=53306, password="123456", database="tsglxt")
            su = con.cursor()
            sql = "INSERT INTO users (passward,id,status)values ('{0}','{1}','{2}')".format(data['passward'],
                                                                                            data['account'],
                                                                                            data['status'])
            su.execute(sql)
        except Exception as e:
            print(e)
        finally:
            con.commit()
            QMessageBox.information(self, "成功", '用户添加成功', QMessageBox.Ok)
            su.close()
            con.close()

    def on_exit(self):
        print("退出")
        sys.exit()
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = TsLogin()
    main.show()
    sys.exit(app.exec_())
