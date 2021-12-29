import sys

import pymysql
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class BookEditWidget(QWidget):
    bookData = {}
    flag = True
    bookDataSignal = pyqtSignal()
    old_isbn = str

    def __init__(self, data={}, flag=True):
        # flag
        super(BookEditWidget, self).__init__()
        self.setWindowModality(Qt.WindowModal)
        self.initUI()
        self.flag = flag
        self.bookData = data
        if not flag:
            self.getBookData()

    def initUI(self):
        self.setWindowTitle("图书信息")
        self.resize(800, 600)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        layout = QGridLayout()

        self.isbnLabel = QLabel("ISBN")
        self.isbnEdit = QLineEdit()

        self.bookNameLabel = QLabel("书名")
        self.bookNameEdit = QLineEdit()

        self.pressLabel = QLabel("出版社")
        self.pressEdit = QLineEdit()

        self.authorLabel = QLabel("作者")
        self.authorEdit = QLineEdit()

        self.storeNumLabel = QLabel("馆藏数量")
        self.storeNumEdit = QLineEdit()

        self.curNumLabel = QLabel("可借数量")
        self.curNumEdit = QLineEdit()

        self.isBorrowAbleLabel = QLabel("是否可借")
        self.isborrowAbleCombox = QComboBox()
        self.isborrowAbleCombox.addItems(['是', '否'])

        self.confirmBtn = QPushButton("确定")

        layout.addWidget(self.isbnLabel, 0, 0, 1, 1, Qt.AlignRight)
        layout.addWidget(self.isbnEdit, 0, 1, 1, 2)

        layout.addWidget(self.bookNameLabel, 0, 3, 1, 1, Qt.AlignRight)
        layout.addWidget(self.bookNameEdit, 0, 4, 1, 2)

        layout.addWidget(self.pressLabel, 1, 0, 1, 1, Qt.AlignRight)
        layout.addWidget(self.pressEdit, 1, 1, 1, 2)

        layout.addWidget(self.authorLabel, 1, 3, 1, 1, Qt.AlignRight)
        layout.addWidget(self.authorEdit, 1, 4, 1, 2)

        layout.addWidget(self.storeNumLabel, 2, 0, 1, 1, Qt.AlignRight)
        layout.addWidget(self.storeNumEdit, 2, 1, 1, 2)

        layout.addWidget(self.curNumLabel, 2, 3, 1, 1, Qt.AlignRight)
        layout.addWidget(self.curNumEdit, 2, 4, 1, 2)

        layout.addWidget(self.isBorrowAbleLabel, 3, 0, 1, 1, Qt.AlignRight)
        layout.addWidget(self.isborrowAbleCombox, 3, 1, 1, 2)

        layout.addWidget(self.confirmBtn, 3, 4, 1, 2)

        self.setLayout(layout)
        self.confirmBtn.clicked.connect(self.alterBookFun)
        pass

    def setBookData(self):
        self.bookData['isbn'] = self.isbnEdit.text()
        self.bookData['bname'] = self.bookNameEdit.text()
        self.bookData['pub'] = self.pressEdit.text()
        self.bookData['author'] = self.authorEdit.text()
        self.bookData['storeNum'] = self.storeNumEdit.text()
        self.bookData['bCurNum'] = self.curNumEdit.text()
        self.bookData['available'] = self.isborrowAbleCombox.currentText()

    def getBookData(self):
        self.isbnEdit.setText(self.bookData['isbn'])
        self.bookNameEdit.setText(self.bookData['bname'])
        self.pressEdit.setText(self.bookData['pub'])
        self.authorEdit.setText(self.bookData['author'])
        self.storeNumEdit.setText(self.bookData['storeNum'])
        self.curNumEdit.setText(self.bookData['bCurNum'])
        self.isborrowAbleCombox.setCurrentText(self.bookData['available'])
        self.old_isbn = self.bookData['isbn']

    def alterBookFun(self):

        if self.flag:
            # 新建书籍函数
            print("新建书籍")
            self.setBookData()
            if len(self.isbnEdit.text())==0:
                QMessageBox.critical(self,'错误',"ISBN号不能为空！",QMessageBox.Ok)
                return
            sql = """
                insert into books(isbn,bname,pub,author,storeNum,bCurNum,available) 
                values ('{}','{}','{}','{}',{},{},'{}')
                """.format(self.bookData['isbn'], self.bookData['bname'], self.bookData['pub'], self.bookData['author'],
                           self.bookData['storeNum'] if len(self.bookData['storeNum']) > 0 else 0,
                           self.bookData['bCurNum'] if len(self.bookData['bCurNum']) > 0 else 0,
                           self.bookData['available'])
            pass
        else:
            print("修改书籍")
            self.setBookData()
            print(self.bookData)
            sql = """
                UPDATE  books set isbn='{0}',bname='{1}',pub='{2}',author='{3}',storeNum={4},bCurNum={5},available='{6}' WHERE isbn='{7}'
            """.format(self.bookData['isbn'], self.bookData['bname'] if len(self.bookData['bname']) else 'None',
                       self.bookData['pub'] if len(self.bookData['pub']) else 'None',
                       self.bookData['author'] if len(self.bookData['author']) else 'None',
                       self.bookData['storeNum'] if len(self.bookData['storeNum']) > 0 else 0,
                       self.bookData['bCurNum'] if len(self.bookData['bCurNum']) > 0 else 0,
                       self.bookData['available'], self.old_isbn)
            print(sql)

            # 修改书籍函数

            pass

        try:
            querySql = """
                                select * from books where isbn='{}'
                                """.format(self.bookData['isbn'])
            conn = pymysql.Connect(host='172.28.22.15', user="root", port=53306, password="123456",
                                   database="tsglxt")
            cur = conn.cursor()
            l = cur.execute(querySql)
            print(l)
            if l > 0 and self.flag:
                QMessageBox.critical(self, '错误', '添加失败！已经存在相同书籍编号的图书！', QMessageBox.Ok)
            elif l == 0 and self.flag:
                l = cur.execute(sql)
                conn.commit()
                QMessageBox.information(self, '成功', '添加书籍成功！', QMessageBox.Ok)
                self.close()
            elif not self.flag:
                l = cur.execute(sql)
                conn.commit()
                QMessageBox.information(self, '成功', '修改书籍信息成功!', QMessageBox.Ok)
                self.close()
            pass
        # except:
        except Exception as e:

            print(e)
        finally:
            cur.close()
            conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = BookEditWidget()
    main.show()
    sys.exit(app.exec_())
