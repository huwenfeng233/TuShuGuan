import json
import sys

import pymysql
from  PyQt5.QtWidgets import *
from  PyQt5.QtCore import *
from  PyQt5.QtGui import *

class RegistryWidget(QWidget):
    registerStatus = pyqtSignal(dict)
    def __init__(self):
        super(RegistryWidget, self).__init__()
        self.registerData={}

        self.initUI()

    def initUI(self):
        self.setWindowTitle("注册页面")
        self.setWindowFlag(Qt.WindowCloseButtonHint)
        layout=QFormLayout()
        self.userLabel=QLabel("账号：")
        self.userLabel.setAlignment(Qt.AlignRight)

        self.passwdLabel=QLabel("密码：")
        self.passwdLabel.setAlignment(Qt.AlignRight)
        self.userLineEdit=QLineEdit(self)
        self.passwdLineEdit=QLineEdit(self)
        self.statusLabel=QLabel("身份：")
        self.statusLabel.setAlignment(Qt.AlignRight)
        self.statuSelect=QComboBox()
        self.statuSelect.addItems(['用户','管理员'])
        self.registerBtn=QPushButton("注册")
        self.registerBtn.clicked.connect(self.on_register_click)
        self.userLabel.setBuddy(self.userLineEdit)

        layout.addRow(self.userLabel,self.userLineEdit)
        layout.addRow(self.passwdLabel,self.passwdLineEdit)
        layout.addRow(self.statusLabel,self.statuSelect)
        layout.addRow(self.registerBtn)
        self.setLayout(layout)
    def on_register_click(self):
        self.registerData['account']=self.userLineEdit.text()
        self.registerData['passward']= self.passwdLineEdit.text()
        self.registerData['status']=self.statuSelect.currentIndex()
        print(self.registerData)
        # self.registerData=json.dump(self.registerData)


        try:
            sql=pymysql.Connect(host='172.28.22.15',user="root",port=53306,password="123456",database="tsglxt")
            cur = sql.cursor()
            data = cur.execute("select * from users where id='{}'".format(self.userLineEdit.text()))
        except Exception as e:
            print(e)

        # print("select * from users where account='{}'".format(self.registerData['account']))
        finally:
            print(cur.fetchall())
            if  data :
                pass
                msg_box = QMessageBox.critical(self, "错误", "用户名已存在，请更换可用的用户名！", buttons=QMessageBox.Ok)
                self.show()
            else:
                # print("用户已经存在")
                print(type(self.registerData))
                self.registerStatus.emit(self.registerData)
                self.close()
                pass
                # print(data)
        print("点击注册按钮")


        pass

if __name__ == '__main__':
    app=QApplication(sys.argv)
    main=RegistryWidget()
    main.show()
    sys.exit(app.exec_())



