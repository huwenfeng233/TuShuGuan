import sys

import pymysql
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ReaderEditWidget(QWidget):
    readerDataSignal = pyqtSignal(dict)

    readerData = {}
    readerHeader = ["borrowid", 'rname', 'sex', 'job', 'rCurNum', 'rBorrowedNum', 'dept', 'phone']

    def __init__(self, data={}, flag=True):
        # 如果flag为true则是新建，否则是修改
        super(ReaderEditWidget, self).__init__()
        self.initUI()
        self.flag = flag
        self.setWindowModality(Qt.WindowModal)
        if len(data.items()) > 2:
            print("更新data")
            try:
                self.borrowIdEdit.setText(data['borrowid'])
                self.deptEdit.setText(data['dept'])
                self.sexBox.setCurrentText(data['sex'])
                self.jobEdit.setText(data['job'])
                self.phoneEdit.setText(data['phone'])
                self.curNumEdit.setText(data['rCurNum'])
                self.borrowedNumEdit.setText(data['rBorrowedNum'])
                self.readerNameEdit.setText(data['rname'])
                self.readerData = data
            except Exception as e:
                print(e)
        self.confirmBtn.clicked.connect(self.on_confirm_Btn)

    def initUI(self):
        self.setWindowTitle("读者编辑")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.resize(800, 600)
        self.setFixedSize(self.width(), self.height());
        self.borrowIdLabel = QLabel("借书证号")
        self.borrowIdEdit = QLineEdit()
        self.readerNameLabel = QLabel("读者姓名")
        self.readerNameEdit = QLineEdit()
        self.sexLabel = QLabel("性别")
        self.sexBox = QComboBox()
        self.sexBox.addItems(["男", "女"])
        self.jobLabel = QLabel("职称")
        self.jobEdit = QLineEdit()
        self.deptLabel = QLabel("部门")
        self.deptEdit = QLineEdit()
        self.phoneLabel = QLabel("电话号码")
        self.phoneEdit = QLineEdit()
        self.accountLabel = QLabel("账号")
        self.accountEdit = QLineEdit()
        self.borrowedNumLabel = QLabel("已借数量")
        self.borrowedNumEdit = QLineEdit()
        self.curNumLabel = QLabel("可借数量")
        self.curNumEdit = QLineEdit()

        self.confirmBtn = QPushButton("确认")

        layout = QGridLayout()
        layout.addWidget(self.borrowIdLabel, 0, 0, 1, 1, Qt.AlignRight)
        layout.addWidget(self.borrowIdEdit, 0, 1, 1, 2)

        layout.addWidget(self.curNumLabel, 0, 3, 1, 1, Qt.AlignRight)
        layout.addWidget(self.curNumEdit, 0, 4, 1, 2, Qt.AlignLeft)

        layout.addWidget(self.readerNameLabel, 1, 0, 1, 1, Qt.AlignRight)
        layout.addWidget(self.readerNameEdit, 1, 1, 1, 2)

        layout.addWidget(self.jobLabel, 2, 0, 1, 1, Qt.AlignCenter)
        layout.addWidget(self.jobEdit, 2, 1, 1, 2)

        # layout.addWidget(self.deptLabel,3,0,1,1)
        # layout.addWidget(self.deptEdit,3,1,1,2,Qt.AlignLeft)

        layout.addWidget(self.sexLabel, 3, 0, 1, 1, Qt.AlignCenter)
        layout.addWidget(self.sexBox, 3, 1, 1, 2)

        layout.addWidget(self.borrowedNumLabel, 1, 3, 1, 1, Qt.AlignRight)
        layout.addWidget(self.borrowedNumEdit, 1, 4, 1, 2)

        layout.addWidget(self.phoneLabel, 2, 3, 1, 1, Qt.AlignRight)
        layout.addWidget(self.phoneEdit, 2, 4, 1, 2)

        layout.addWidget(self.deptLabel, 3, 3, 1, 1, Qt.AlignRight)
        layout.addWidget(self.deptEdit, 3, 4, 1, 2)

        layout.addWidget(self.confirmBtn, 4, 2, 1, 3, Qt.AlignHCenter)
        self.setLayout(layout)

        pass

    def on_confirm_Btn(self):
        if len(self.borrowIdEdit.text()) == 0:
            QMessageBox.critical(self, "错误", '必须输入借书证号', QMessageBox.Ok)
        else:
            try:
                sql = """
                    SELECT * FROM readers WHERE borrowid='{}';
                    """.format(self.borrowIdEdit.text())
                print(sql)
                con = pymysql.Connect(host='172.28.22.15', user="root", port=53306, password="123456",
                                      database="tsglxt")
                cur = con.cursor()
                l = cur.execute(sql)
                # 如果用户已经存在，则发出提示
                if l > 0 and self.flag:
                    QMessageBox.critical(self, '错误', '用户已经存在！', QMessageBox.Ok)
                else:
                    self.updateReader(self.flag)

            except Exception as e:
                print(e)

        print("点击确认按钮")

        pass

    def updateReader(self, flag=bool):
        # bool=1插入 bool=0为更新
        print(self.readerData)
        self.readerData[self.readerHeader[0]] = self.borrowIdEdit.text()
        self.readerData[self.readerHeader[1]] = self.readerNameEdit.text()
        self.readerData[self.readerHeader[2]] = self.sexBox.currentText()
        self.readerData[self.readerHeader[3]] = self.jobEdit.text()
        self.readerData[self.readerHeader[4]] = self.curNumEdit.text()
        self.readerData[self.readerHeader[5]] = self.borrowedNumEdit.text()
        self.readerData[self.readerHeader[6]] = self.deptEdit.text()
        self.readerData[self.readerHeader[7]] = self.phoneEdit.text()
        try:
            if not flag:
                print("新增读者")
                sql = """
                UPDATE readers set borrowid='{0}' ,rname='{1}',sex='{2}',job='{3}',rCurNum={4},
                rBorrowedNum={5},dept='{6}',phone='{7}'
                """.format(self.readerData['borrowid'], self.readerData['rname'], self.readerData['sex'],
                           self.readerData['job'], self.readerData['rCurNum'], self.readerData['rBorrowedNum'],
                           self.readerData['dept'], self.readerData['phone'])
            else:
                sql = """
                    INSERT INTO readers(borrowid,rname,sex,job,rCurNum,
                rBorrowedNum,dept,phone)  values ('{0}' ,'{1}','{2}','{3}',{4},
                {5},'{6}','{7}')
                    """.format(self.readerData['borrowid'], self.readerData['rname'], self.readerData['sex'],
                               self.readerData['job'], self.readerData['rCurNum'], self.readerData['rBorrowedNum'],
                               self.readerData['dept'], self.readerData['phone'])
            print(sql)
            con = pymysql.Connect(host='172.28.22.15', user="root", port=53306, password="123456",
                                  database="tsglxt")
            cur = con.cursor()
            l = cur.execute(sql)
            con.commit()
            choice = QMessageBox.information(self, '成功', '更新成功!', QMessageBox.Ok)
            if choice == QMessageBox.Ok:
                print(self.readerData)
                self.readerDataSignal.emit(self.readerData)
                pass
            self.close()
            # return

        except Exception as e:
            print(e)
        print("更新或插入操作")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = ReaderEditWidget()
    main.show()
    sys.exit(app.exec_())
