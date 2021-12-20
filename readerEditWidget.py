import sys

from  PyQt5.QtWidgets import *
from  PyQt5.QtCore import *
from  PyQt5.QtGui import *


class ReaderEditWidget(QWidget):
    def __init__(self):
        super(ReaderEditWidget, self).__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle("读者编辑")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.resize(800,600)
        self.setFixedSize(self.width(), self.height());
        self.borrowIdLabel=QLabel("借书证号")
        self.borrowIdEdit=QLineEdit()
        self.readerNameLabel=QLabel("读者姓名")
        self.readerNameEdit=QLineEdit()
        self.sexLabel=QLabel("性别")
        self.sexBox=QComboBox()
        self.sexBox.addItems(["男","女"])
        self.jobLabel=QLabel("职称")
        self.jobEdit=QLineEdit()
        self.deptLabel=QLabel("部门")
        self.deptEdit=QLineEdit()
        self.phoneLabel=QLabel("电话号码")
        self.phoneEdit=QLineEdit()
        self.accountLabel=QLabel("账号")
        self.accountEdit=QLineEdit()
        self.borrowedNumLabel=QLabel("已借数量")
        self.borrowedNumEdit=QLineEdit()
        self.curNumLabel=QLabel("可借数量")
        self.curNumEdit=QLineEdit()

        self.confirmBtn=QPushButton("确认")

        layout=QGridLayout()
        layout.addWidget(self.borrowIdLabel,0,0,1,1)
        layout.addWidget(self.borrowIdEdit,0,1,1,1,Qt.AlignLeft)

        layout.addWidget(self.curNumLabel,0,3,1,1)
        layout.addWidget(self.curNumEdit,0,4,1,2,Qt.AlignLeft)

        layout.addWidget(self.readerNameLabel,1,0,1,1)
        layout.addWidget(self.readerNameEdit,1,1,1,2,Qt.AlignLeft)

        layout.addWidget(self.jobLabel,2,0,1,1)
        layout.addWidget(self.jobEdit,2,1,1,2,Qt.AlignLeft)

        layout.addWidget(self.deptLabel,3,0,1,1)
        layout.addWidget(self.deptEdit,3,1,1,2,Qt.AlignLeft)

        layout.addWidget(self.sexLabel,4,0,1,1)
        layout.addWidget(self.sexBox,4,1,1,2)


        layout.addWidget(self.borrowedNumLabel,1,3,1,1)
        layout.addWidget(self.borrowedNumEdit,1,4,1,2,Qt.AlignLeft)


        layout.addWidget(self.phoneLabel,2,3,1,1)
        layout.addWidget(self.phoneEdit,2,4,1,2,Qt.AlignLeft)

        layout.addWidget(self.accountLabel,3,3,1,1)
        layout.addWidget(self.accountEdit,3,4,1,2,Qt.AlignLeft)

        layout.addWidget(self.confirmBtn,4,4,1,1,Qt.AlignHCenter)
        self.setLayout(layout)

        pass
    def on_confirm_Btn(self):
        print("点击确认按钮")
        pass
if __name__ == '__main__':
    app=QApplication(sys.argv)
    main=ReaderEditWidget()
    main.show()
    sys.exit(app.exec_())