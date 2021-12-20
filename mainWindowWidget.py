import sys

import pymysql

import bookEditWidget
import LoginWidget
import readerEditWidget

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MainWindowWidget(QMainWindow):
    readerData = {}
    readerData["borrowid"] = 0
    readerData['rname'] = 0
    readerData['sex'] = 0
    readerData['job'] = 0
    readerData['rCurNum'] = 0
    readerData['rBorrowedNum'] = 0
    readerData['dept'] = 0
    readerData['phone'] = 0

    bookData = {}
    readerHeader = ["borrowid", 'rname', 'sex', 'job', 'rCurNum', 'rBorrowedNum', 'dept', 'phone' ]
    Header = [['账号', '昵称', '性别', '职称', '当前可借数量', '已借数量', '工作部门', '电话'],
              ['ISBN', '书名', '出版社', '作者', '馆藏数量', '目前数量', '是否可借'],
              ['借书证号', '图书编号', '借书日期', '间隔', '还书日期', '罚金']]

    def __init__(self):
        super(MainWindowWidget, self).__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("查询&管理")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.resize(1366, 768)

        self.tabMainWidget = QTabWidget()
        self.setCentralWidget(self.tabMainWidget)
        self.tabWidget1 = QWidget(self)
        self.tabWidget2 = QWidget(self)
        self.tabWidget3 = QWidget(self)
        self.initTabWidget()
        pass

    def initTabWidget(self):
        self.tabMainWidget.addTab(self.tabWidget1, "读者信息")
        self.tabMainWidget.addTab(self.tabWidget2, "图书信息")
        self.tabMainWidget.addTab(self.tabWidget3, "逾期图书信息")
        self.initFirstTab()
        self.initSecondTab()
        self.initThirdTab()

        # 初始化第一个标签页

    def initFirstTab(self):
        self.queryReaderConditionWidget = QGroupBox()
        self.queryReaderConditionWidget.setTitle("查询条件")
        layout1 = QVBoxLayout()
        layout1.addWidget(self.queryReaderConditionWidget)
        self.tabWidget1.setLayout(layout1)
        self.borrowIdLable = QLabel("借书证号")
        self.borrowIdEdit = QLineEdit()
        self.nameLabel = QLabel("姓名")
        self.nameEdit = QLineEdit()
        self.sexLabel = QLabel("性别")
        self.sexCombox = QComboBox()
        self.sexCombox.addItems([' ', '男', '女'])
        self.jobLabel = QLabel("职称")
        self.jobEdit = QLineEdit()

        self.deptLabel = QLabel("工作部门")
        self.deptEdit = QLineEdit()
        self.phonelabel = QLabel("电话号码")
        self.phoneEdit = QLineEdit()

        self.accountLabel = QLabel("账户")
        self.accountEdit = QLineEdit()

        self.curNumLabel = QLabel("最少可借数量")
        self.curNumEdit = QLineEdit()

        self.borrowedNumLabel = QLabel("最少已借数量")
        self.borrowedNumEdit = QLineEdit()

        self.queryReaderBtn = QPushButton("查询")
        subLayout = QGridLayout()
        subLayout.addWidget(self.borrowIdLable, 0, 0, 1, 1, Qt.AlignRight)
        subLayout.addWidget(self.borrowIdEdit, 0, 1, 1, 2)
        subLayout.addWidget(self.nameLabel, 0, 3, 1, 1, Qt.AlignRight)
        subLayout.addWidget(self.nameEdit, 0, 4, 1, 2)
        subLayout.addWidget(self.sexLabel, 0, 6, 1, 1, Qt.AlignRight)
        subLayout.addWidget(self.sexCombox, 0, 7, 1, 2)
        subLayout.addWidget(self.jobLabel, 0, 9, 1, 1, Qt.AlignRight)
        subLayout.addWidget(self.jobEdit, 0, 10, 1, 2)
        subLayout.addWidget(self.curNumLabel, 1, 0, 1, 1, Qt.AlignRight)
        subLayout.addWidget(self.curNumEdit, 1, 1, 1, 2)
        subLayout.addWidget(self.borrowedNumLabel, 1, 3, 1, 1, Qt.AlignRight)
        subLayout.addWidget(self.borrowedNumEdit, 1, 4, 1, 2)
        subLayout.addWidget(self.deptLabel, 1, 6, 1, 1, Qt.AlignRight)
        subLayout.addWidget(self.deptEdit, 1, 7, 1, 2)
        subLayout.addWidget(self.phonelabel, 1, 9, 1, 1, Qt.AlignRight)
        subLayout.addWidget(self.phoneEdit, 1, 10, 1, 2)

        subLayout.addWidget(self.queryReaderBtn, 2, 1, 1, 1)
        self.queryReaderConditionWidget.setLayout(subLayout)
        self.queryResultWidget = QGroupBox()
        self.queryResultWidget.setTitle("查询结果")
        queryResultWidgetLayout = QHBoxLayout()

        self.queryResultTable = QTableWidget()
        queryResultWidgetLayout.addWidget(self.queryResultTable)

        # layout1.addWidget(self.queryResultWidget)
        layout1.addLayout(queryResultWidgetLayout)
        self.newReaderBtn = QPushButton("新增")
        self.delReaderBtn = QPushButton("删除")
        self.alterReaderBtn = QPushButton("编辑")

        btnLayout = QHBoxLayout()
        btnLayout.addWidget(self.newReaderBtn, alignment=Qt.AlignLeft)
        btnLayout.addWidget(self.delReaderBtn, alignment=Qt.AlignCenter)
        btnLayout.addWidget(self.alterReaderBtn, alignment=Qt.AlignRight)
        layout1.addLayout(btnLayout)
        self.queryReaderBtn.clicked.connect(self.queryReaderFun)
        self.newReaderBtn.clicked.connect(self.on_newReaderClick)
        self.delReaderBtn.clicked.connect(self.on_delReaderClick)
    # 初始化第二个标签页
    def initSecondTab(self):
        layout2 = QVBoxLayout()
        subLayout = QVBoxLayout()
        self.tabWidget2.setLayout(layout2)
        # self.tabWidget2.setLayout(subLayout)
        self.queryBookSConditionGroupBox = QGroupBox()
        self.queryBookSConditionGroupBox.setTitle("查询条件")
        self.queryBookSConditionGroupBox.setLayout(subLayout)
        layout2.addWidget(self.queryBookSConditionGroupBox)
        isbnLabel = QLabel("ISBN书号")
        self.isbnEdit = QLineEdit()

        bookNameLabel = QLabel("书名")
        self.bookNameEdit = QLineEdit()

        pressLabel = QLabel("出版社")
        self.pressEdit = QLineEdit()

        authorLabel = QLabel("作者")
        self.authorEdit = QLineEdit()

        curNumLabel = QLabel("最少可借数量")
        self.curNumEdit = QLineEdit()

        saveNumLabel = QLabel("最少馆藏数量")
        self.saveNumEdit = QLineEdit()

        isBorrowAbelLabel = QLabel("是否可借")

        self.isBorrowAbleComBox = QComboBox()
        self.isBorrowAbleComBox.addItems(["是", '否'])

        queryBtn = QPushButton("查询")

        subLayoutR1 = QHBoxLayout()
        subLayoutR1.addWidget(isbnLabel)
        subLayoutR1.addWidget(self.isbnEdit)
        subLayoutR1.addWidget(bookNameLabel)
        subLayoutR1.addWidget(self.bookNameEdit)
        subLayoutR1.addWidget(pressLabel)
        subLayoutR1.addWidget(self.pressEdit)

        subLayoutR2 = QHBoxLayout()
        subLayoutR2.addWidget(authorLabel)
        subLayoutR2.addWidget(self.authorEdit)
        subLayoutR2.addWidget(curNumLabel)
        subLayoutR2.addWidget(self.curNumEdit)

        subLayoutR3 = QHBoxLayout()
        subLayoutR3.addWidget(saveNumLabel)
        subLayoutR3.addWidget(self.saveNumEdit)
        subLayoutR3.addWidget(isBorrowAbelLabel)
        subLayoutR3.addWidget(self.isBorrowAbleComBox)

        subLayout.addLayout(subLayoutR1)
        subLayout.addLayout(subLayoutR2)
        subLayout.addLayout(subLayoutR3)
        subLayout.addWidget(queryBtn)

        self.queryBookSConditionGroupBox.setLayout(subLayout)
        self.newBookBtn = QPushButton("新增")
        self.borrowBookBtn = QPushButton("借书")
        self.delBookBtn = QPushButton("删除")
        self.returnBookBtn = QPushButton("还书")
        self.editBookBtn = QPushButton("编辑")
        btnLayout = QHBoxLayout()
        btnLayout.addWidget(self.newBookBtn)
        btnLayout.addWidget(self.borrowBookBtn)
        btnLayout.addWidget(self.delBookBtn)
        btnLayout.addWidget(self.returnBookBtn)
        btnLayout.addWidget(self.editBookBtn)

        self.queryBookResultGroupBox = QGroupBox()
        self.queryBookResultGroupBox.setTitle("查询结果")
        self.queryBookResultTableWidget = QTableWidget()
        groupBoxLayou = QVBoxLayout()
        groupBoxLayou.addWidget(self.queryBookResultTableWidget)
        self.queryBookResultGroupBox.setLayout(groupBoxLayou)
        layout2.addWidget(self.queryBookResultTableWidget)
        layout2.addLayout(btnLayout)
        queryBtn.clicked.connect(self.queryBooksFun)

    def initThirdTab(self):
        self.queryOutDateGroupBox = QGroupBox()
        self.queryOutDateGroupBox.setTitle("查询结果")
        self.queryOutDateTabel = QTableWidget()
        queryBtn = QPushButton("查询")
        layout = QVBoxLayout()
        layout.addWidget(self.queryOutDateTabel)
        self.queryOutDateGroupBox.setLayout(layout)
        subLayout = QVBoxLayout()
        subLayout.addWidget(self.queryOutDateGroupBox)
        subLayout.addWidget(queryBtn)
        self.tabWidget3.setLayout(subLayout)
        queryBtn.clicked.connect(self.queryOutDateBooks)
        pass

    def queryReaderFun(self):
        self.readerData["borrowid"] = self.borrowIdEdit.text()
        self.readerData['rname'] = self.nameEdit.text()
        self.readerData['sex'] = self.sexCombox.currentText()
        self.readerData['job'] = self.jobEdit.text()
        self.readerData['rCurNum'] = self.curNumEdit.text()
        self.readerData['rBorrowedNum'] = self.borrowedNumEdit.text()
        self.readerData['dept'] = self.deptEdit.text()
        self.readerData['phone'] = self.phoneEdit.text()
        self.readerData['account'] = self.accountEdit.text()
        print(self.readerData)

        self.queryResultTable.clear()
        self.queryResultTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.queryResultTable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        try:
            sql = """
                SELECT * FROM readers
                WHERE borrowid like '%{0}%' and rname like '%{1}%' 
                and sex in('男','女',null) 
                and (job like '%{3}%' or job is null )  
                and (dept like '%{6}%' or dept is null ) 
                and (phone like '%{7}%' or phone is null );
                """.format(self.readerData["borrowid"], self.readerData['rname'], self.readerData['sex'],
                           self.readerData['job'],
                           0 if len(self.readerData['rCurNum']) == 0 else self.readerData['rCurNum'],
                           0 if len(self.readerData['rBorrowedNum']) == 0 else self.readerData['rBorrowedNum'],
                           self.readerData['dept'], self.readerData['phone'], self.readerData['account'])
            # print(sql)
            "and account like '%{8}%'"
            sql2 = """SELECT * FROM readers WHERE  RNAME LIKE '%{}%' and phone like '%{}%'  """.format('胡', '17')
            con = pymysql.Connect(host='172.28.22.15', user="root", port=53306, password="123456", database="tsglxt")
            cu = con.cursor()

            res = cu.execute(sql)
            print()
            a=0
            self.queryResultTable.setColumnCount(len(self.Header[0]))
            for i in self.Header[0]:

                print(i)
                item = QTableWidgetItem(str(i))
                self.queryResultTable.setHorizontalHeaderItem(a, item)
                a += 1
            if res > 0:
                colResult = cu.description
                res_data = cu.fetchall()
                col = len(res_data[0])

                print(res_data)
                row = cu.rowcount
                print(row, col)

                self.queryResultTable.setRowCount(row)


                for i in range(0, row):
                    for j in range(0, col):
                        self.queryResultTable.setItem(i, j, QTableWidgetItem(str(res_data[i][j])))
            # print(res)
            # print(cu.fetchall())

        except Exception as e:
            print(e)
            pass
        finally:
            con.commit()
            cu.close()
            con.close()
            pass
        # pass

    def queryBooksFun(self, book: map):
        self.queryBookResultTableWidget.clear()
        self.queryBookResultTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.queryBookResultTableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.bookData['isbn'] = self.isbnEdit.text()
        self.bookData['bname'] = self.bookNameEdit.text()
        self.bookData['pub'] = self.pressEdit.text()
        self.bookData['author'] = self.authorEdit.text()
        self.bookData['storeNum'] = self.saveNumEdit.text()
        self.bookData['bCurNum'] = self.curNumEdit.text()
        self.bookData['available'] = self.isBorrowAbleComBox.currentText()
        print(self.bookData)

        # print(self.bookData)
        sql = r"""
            SELECT * FROM books where isbn like '%{0}%' and bname like '%{1}%' and pub like '%{2}%' 
            and author like '%{3}%' and storeNum >={4} and bCurNum>={5} and available='{6}';
            """.format(self.bookData['isbn'], self.bookData['bname'], self.bookData['pub'], self.bookData['author'],
                       self.bookData['storeNum'] if len(self.bookData['storeNum']) != 0 else 0,
                       self.bookData['bCurNum'] if len(self.bookData['bCurNum']) != 0 else 0,
                       self.bookData['available'])
        print(sql)
        try:
            con = pymysql.connect(host='172.28.22.15', user="root", port=53306, password="123456", database="tsglxt")
            cur = con.cursor()
            res = cur.execute(sql)

            if res > 0:
                data = cur.fetchall()
                colData = cur.description
                # print(colData)
                row = cur.rowcount
                col = len(data[0])
                self.queryBookResultTableWidget.setColumnCount(col)
                self.queryBookResultTableWidget.setRowCount(row)
                print(row, col)
                print(data)
                a = 0
                for i in self.Header[1]:
                    # print(i[0])
                    self.queryBookResultTableWidget.setHorizontalHeaderItem(a, QTableWidgetItem(str(i)))
                    a += 1
                for i in range(0, row):
                    for j in range(0, col):
                        self.queryBookResultTableWidget.setItem(i, j, QTableWidgetItem(str(data[i][j])))
            pass
        except Exception as e:
            cur.close()
            con.close()
            print(e)
        pass

    def queryOutDateBooks(self):
        self.queryOutDateTabel.clear()
        self.queryOutDateTabel.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.queryOutDateTabel.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        sql = """
            SELECT * FROM rb WHERE curdate()-rb.startDate>rb.duration;
            """
        try:
            con = pymysql.connect(host='172.28.22.15', user="root", port=53306, password="123456", database="tsglxt")
            cur = con.cursor()
            res = cur.execute(sql)
            data = cur.fetchall()
            print(data)
            # cur.execute('')
            print()
            if res > 0:
                row = cur.rowcount
                col = len(data[0])
                print(col)
                self.queryOutDateTabel.setColumnCount(col)
                self.queryOutDateTabel.setRowCount(row)
                a = 0
                for i in self.Header[2]:
                    # print(i)
                    self.queryOutDateTabel.setHorizontalHeaderItem(a, QTableWidgetItem(str(i)))
                    a += 1
                for i in range(0, row):
                    for j in range(0, col):
                        self.queryOutDateTabel.setItem(i, j, QTableWidgetItem(str(data[i][j])))
        except Exception as e:
            cur.close()
            con.close()
            print(e)

    # 新增读者函数
    def on_newReaderClick(self):
        self.newReaderWidget = readerEditWidget.ReaderEditWidget()
        self.newReaderWidget.show()
        pass

    # 删除读者函数
    def on_delReaderClick(self):
        curRow = self.queryResultTable.currentRow()
        try:
            for i in range(len(self.readerHeader)):
                self.readerData[self.readerHeader[i]]=self.queryResultTable.item(curRow,i ).text()

                print(i,self.queryResultTable.item(curRow, i).text())
            # print(self.readerData)
            sql="""
                DELETE FROM readers where borrowid={}
                """.format(self.readerData['borrowid'])
            con=pymysql.connect(host='172.28.22.15', user="root", port=53306, password="123456", database="tsglxt")
            cur=con.cursor()
            cur.execute(sql)
            con.commit()
            QMessageBox().information(self,'成功','删除读者信息成功!',QMessageBox.Ok)
            print(sql)
        except Exception as e:
            print(e)
        finally:
            cur.close()
            con.close()
            self.queryReaderFun()
        pass

    # 修改读者信息函数
    def on_alterReaderClick(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindowWidget()
    main.show()
    sys.exit(app.exec_())
