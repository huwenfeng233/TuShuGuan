import sys

from  PyQt5.QtWidgets import *
from  PyQt5.QtCore import *
from  PyQt5.QtGui import *


class BookEditWidget(QWidget):
    def __init__(self):
        super(BookEditWidget, self).__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle("图书信息")
        self.resize(800,600)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        layout=QGridLayout()

        self.isbnLabel=QLabel("ISBN")
        self.isbnEdit=QLineEdit()

        self.bookNameLabel=QLabel("书名")
        self.bookNameEdit=QLineEdit()

        self.pressLabel=QLabel("出版社")
        self.pressEdit=QLineEdit()

        self.authorLabel=QLabel("作者")
        self.authorEdit=QLineEdit()

        self.storeNumLabel=QLabel("馆藏数量")
        self.storeNumEdit=QLineEdit()

        self.curNumLabel=QLabel("可借数量")
        self.curNumEdit=QLineEdit()

        self.isBorrowAbleLabel=QLabel("是否可借")
        self.isborrowAbleCombox=QComboBox()
        self.isborrowAbleCombox.addItems(['是','否'])

        self.confirmBtn=QPushButton("确定")

        layout.addWidget(self.isbnLabel,0,0,1,1,Qt.AlignRight)
        layout.addWidget(self.isbnEdit,0,1,1,2)
        
        layout.addWidget(self.bookNameLabel,0,3,1,1,Qt.AlignRight)
        layout.addWidget(self.bookNameEdit,0,4,1,2)
        
        layout.addWidget(self.pressLabel,1,0,1,1,Qt.AlignRight)
        layout.addWidget(self.pressEdit,1,1,1,2)
        
        layout.addWidget(self.authorLabel,1,3,1,1,Qt.AlignRight)
        layout.addWidget(self.authorEdit,1,4,1,2)

        layout.addWidget(self.storeNumLabel,2,0,1,1,Qt.AlignRight)
        layout.addWidget(self.storeNumEdit,2,1,1,2)

        layout.addWidget(self.curNumLabel,2,3,1,1,Qt.AlignRight)
        layout.addWidget(self.curNumEdit,2,4,1,2)

        layout.addWidget(self.isBorrowAbleLabel,3,0,1,1,Qt.AlignRight)
        layout.addWidget(self.isborrowAbleCombox,3,1,1,2)
        
        layout.addWidget(self.confirmBtn,3,4,1,2)

        self.setLayout(layout)
        
        pass

if __name__ == '__main__':
    app=QApplication(sys.argv)
    main=BookEditWidget()
    main.show()
    sys.exit(app.exec_())