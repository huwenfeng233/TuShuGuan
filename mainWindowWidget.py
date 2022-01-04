import sys

import pymysql

import bookEditWidget
import LoginWidget
import readerEditWidget

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MainWindowWidget(QMainWindow):
    currentUserid = str
    mysql = {"host": '172.28.22.15', 'user': "root", "port": 53306, "password": "123456", "database": "tsglxt"}
    # 0为查询过后的状态,1为按下还书键后的状态,2为选择了要还的书籍的状态
    returnStatus = 0
    date = str
    maxBorrowDay = 30
    currentUserStatus = str
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
    readerHeader = ["borrowid", 'rname', 'sex', 'job', 'rCurNum', 'rBorrowedNum', 'dept', 'phone']
    Header = [['账号', '昵称', '性别', '职称', '当前可借数量', '已借数量', '工作部门', '电话'],
              ['ISBN', '书名', '出版社', '作者', '馆藏数量', '可借数量', '是否可借'],
              ['借书证号', '图书编号', '借书日期', '间隔', '还书日期', '罚金']]
    sendData = pyqtSignal(dict)

    def __init__(self, userid: str, userStatus: str):
        super(MainWindowWidget, self).__init__()

        self.currentUserid = userid
        # 0为普通用户，1为管理员
        self.currentUserStatus = userStatus
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
        if self.currentUserStatus == 1:
            layout1.addLayout(btnLayout)
        self.queryReaderBtn.clicked.connect(self.queryReaderFun)
        self.newReaderBtn.clicked.connect(self.on_newReaderClick)
        self.delReaderBtn.clicked.connect(self.on_delReaderClick)
        self.alterReaderBtn.clicked.connect(self.on_alterReaderClick)

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

        if self.currentUserStatus == 1:
            btnLayout.addWidget(self.newBookBtn)

            btnLayout.addWidget(self.delBookBtn)

            btnLayout.addWidget(self.editBookBtn)
        else:
            btnLayout.addWidget(self.borrowBookBtn)
            btnLayout.addWidget(self.returnBookBtn)

        self.queryBookResultGroupBox = QGroupBox()
        self.queryBookResultGroupBox.setTitle("查询结果")
        self.queryBookResultTableWidget = QTableWidget()
        groupBoxLayou = QVBoxLayout()
        groupBoxLayou.addWidget(self.queryBookResultTableWidget)
        self.queryBookResultGroupBox.setLayout(groupBoxLayou)
        layout2.addWidget(self.queryBookResultTableWidget)
        layout2.addLayout(btnLayout)
        queryBtn.clicked.connect(self.queryBooksFun)

        self.newBookBtn.clicked.connect(self.newBookFun)
        self.editBookBtn.clicked.connect(self.alterBookFun)
        self.delBookBtn.clicked.connect(self.delBookFun)
        self.borrowBookBtn.clicked.connect(self.on_borrowBtn_clicked)
        self.returnBookBtn.clicked.connect(self.on_returnBtn_clicked)

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

            con = pymysql.Connect(host='47.93.21.11', user="root", port=3306, password="lovemiss1314",
                                  database="tsglxt")
            cu = con.cursor()

            res = cu.execute(sql)
            print()
            a = 0
            self.queryResultTable.setColumnCount(len(self.Header[0]))

            self.queryResultTable.setHorizontalHeaderLabels(self.Header[0])
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

    def setBookData(self):
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

    def queryBooksFun(self, book: map):
        self.setBookData()
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
            con = pymysql.connect(host='47.93.21.11', user="root", port=3306, password="lovemiss1314",
                                  database="tsglxt")
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
                self.queryBookResultTableWidget.setHorizontalHeaderLabels(self.Header[1])
                # a = 0
                # for i in self.Header[1]:
                #     # print(i[0])
                #     self.queryBookResultTableWidget.setHorizontalHeaderItem(a, QTableWidgetItem(str(i)))
                #     a += 1
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
        if self.currentUserStatus == 1:
            sql = """
            SELECT borrowid, isbn, startDate, DATEDIFF( curdate(),rb.startDate), returnDate, fine FROM rb WHERE curdate()-rb.startDate>{};
            """.format(self.maxBorrowDay)
        else:
            sql = """
                SELECT borrowid, isbn, startDate, DATEDIFF( curdate(),rb.startDate), returnDate, fine FROM rb WHERE curdate()-rb.startDate>{} and borrowid='{}';
                """.format(self.maxBorrowDay, self.currentUserid)
        try:
            con = pymysql.connect(host='47.93.21.11', user="root", port=3306, password="lovemiss1314",
                                  database="tsglxt")
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
                self.queryOutDateTabel.setHorizontalHeaderLabels(self.Header[2])
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
        self.newReaderWidget.readerDataSignal.connect(self.queryReaderFun)
        self.newReaderWidget.show()

        pass

    # 删除读者函数
    def on_delReaderClick(self):
        curRow = self.queryResultTable.currentRow()
        try:
            for i in range(len(self.readerHeader)):
                self.readerData[self.readerHeader[i]] = self.queryResultTable.item(curRow, i).text()

                print(i, self.queryResultTable.item(curRow, i).text())
            # print(self.readerData)
            sql = """
                DELETE FROM readers where borrowid='{}'
                """.format(self.readerData['borrowid'])
            con = pymysql.connect(host='47.93.21.11', user="root", port=3306, password="lovemiss1314",
                                  database="tsglxt")
            cur = con.cursor()
            cur.execute(sql)
            con.commit()
            QMessageBox().information(self, '成功', '删除读者信息成功!', QMessageBox.Ok)
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
        row = self.queryResultTable.currentRow()
        if row >= 0:
            try:
                # self.setBookData()
                # print(row)
                self.readerData["borrowid"] = self.queryResultTable.item(row, 0).text()
                self.readerData['rname'] = self.queryResultTable.item(row, 1).text()
                self.readerData['sex'] = self.queryResultTable.item(row, 2).text()
                self.readerData['job'] = self.queryResultTable.item(row, 3).text()
                self.readerData['rCurNum'] = self.queryResultTable.item(row, 4).text()
                self.readerData['rBorrowedNum'] = self.queryResultTable.item(row, 5).text()
                self.readerData['dept'] = self.queryResultTable.item(row, 6).text()
                self.readerData['phone'] = self.queryResultTable.item(row, 7).text()
                print(self.readerData)
                self.newReaderWidget = readerEditWidget.ReaderEditWidget(self.readerData, False)
                self.newReaderWidget.readerDataSignal.connect(self.queryReaderFun)
                self.newReaderWidget.show()
            # self.readerData['account'] = self.queryResultTable.item(row,0).text()
            except Exception as e:
                print(e)

            # self.queryReaderFun()

        else:
            QMessageBox.critical(self, '错误', '请先查询或者新建用户！', QMessageBox.Ok)
        pass

    def newBookFun(self):
        self.bookEditWidget = bookEditWidget.BookEditWidget()
        self.bookEditWidget.show()

    def delBookFun(self):
        if self.queryBookResultTableWidget.currentRow() == -1:
            QMessageBox.critical(self, '错误', '请先选择一个书籍', QMessageBox.Ok)
            return
        isbn = self.queryBookResultTableWidget.item(self.queryBookResultTableWidget.currentRow(), 0).text()

        print(isbn)
        sql = """
            delete from books where isbn='{}'
            """.format(isbn)
        try:
            conn = pymysql.Connect(host='47.93.21.11', user="root", port=3306, password="lovemiss1314",
                                   database="tsglxt")
            cur = conn.cursor()
            l = cur.execute(sql)
            choice = QMessageBox.information(self, '确认', '确定要删除吗?', QMessageBox.Ok | QMessageBox.Cancel)
            if choice == QMessageBox.Ok:
                conn.commit()
                print("删除书籍信息")
                self.queryBooksFun(self.bookData)
            else:
                pass
        except  Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()

        pass

    def alterBookFun(self):
        if self.queryBookResultTableWidget.currentRow() == -1:
            QMessageBox.critical(self, '错误', '请先选择一个书籍', QMessageBox.Ok)
            return
        isbn = self.queryBookResultTableWidget.item(self.queryBookResultTableWidget.currentRow(), 0).text()
        self.bookData['isbn'] = self.queryBookResultTableWidget.item(self.queryBookResultTableWidget.currentRow(),
                                                                     0).text()
        self.bookData['bname'] = self.queryBookResultTableWidget.item(self.queryBookResultTableWidget.currentRow(),
                                                                      1).text()
        self.bookData['pub'] = self.queryBookResultTableWidget.item(self.queryBookResultTableWidget.currentRow(),
                                                                    2).text()
        self.bookData['author'] = self.queryBookResultTableWidget.item(self.queryBookResultTableWidget.currentRow(),
                                                                       3).text()
        self.bookData['storeNum'] = self.queryBookResultTableWidget.item(self.queryBookResultTableWidget.currentRow(),
                                                                         4).text()
        self.bookData['bCurNum'] = self.queryBookResultTableWidget.item(self.queryBookResultTableWidget.currentRow(),
                                                                        5).text()
        self.bookData['availabel'] = self.queryBookResultTableWidget.item(self.queryBookResultTableWidget.currentRow(),
                                                                          6).text()
        print(self.bookData)
        sql = """
            select * from books where isbn='{}'
            """.format(isbn)
        try:

            self.alterBookWidget = bookEditWidget.BookEditWidget(self.bookData, False)
            self.alterBookWidget.show()

        except  Exception as e:
            print(e)

    def on_borrowBtn_clicked(self):
        print("借书按钮被按下")
        if self.returnStatus == 1:
            QMessageBox.warning(self, '错误', '请先查询书籍!', QMessageBox.Ok)
            self.returnStatus = 0
            return

        query_sql = """
            SELECT * FROM rb where  borrowid='{}'
            """.format(self.currentUserid)
        row = self.queryBookResultTableWidget.currentRow()
        if row == -1:
            QMessageBox.critical(self, '错误', '请先选择要借的书籍！', QMessageBox.Ok)
            return
        curNum = int(self.queryBookResultTableWidget.item(row, 5).text())
        print("剩余数量：", curNum)
        if curNum == 0:
            QMessageBox.critical(self, '错误', '书籍已经全部借出，操作失败！', QMessageBox.Ok)
            return
        try:
            conn = pymysql.Connect(host='47.93.21.11', user="root", port=3306, password="lovemiss1314",
                                   database="tsglxt")
            cur = conn.cursor()
            length = cur.execute(query_sql)
            if length == 5:
                QMessageBox.warning(self, '错误', '用户借书数量已经到达最大上限，请先还书后再进行借书操作', QMessageBox.Ok)
            else:
                self.dateBtn = QPushButton("确定")
                self.dateBtn.clicked.connect(self.borrowBookFun)
                self.dateWidget = QWidget()
                self.dateWidget.resize(400, 200)

                self.dateWidget.setWindowFlags(Qt.WindowCloseButtonHint)
                self.dateWidget.setWindowTitle("选择借书日期")
                self.dateWidget.setWindowModified(True)
                self.calendar = QDateEdit()
                self.calendar.setCalendarPopup(True)
                self.calendar.setDate(QDate.currentDate())
                self.layout = QVBoxLayout()
                self.layout.addWidget(self.calendar)
                self.dateWidget.setLayout(self.layout)
                self.dateWidget.show()
                self.layout.addWidget(self.dateBtn)
                self.calendar.show()

                # print(self.date)
            pass
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()
            pass

    def borrowBookFun(self):
        self.date = self.calendar.text()
        print(self.date)
        self.dateWidget.close()
        try:

            sql = """
                    insert into rb(borrowid,isbn,duration,startDate) values ('{0}','{1}',{2},str_to_date('{3}-{4}-{5}', '%Y-%m-%d'))
                    """.format(self.currentUserid,
                               self.queryBookResultTableWidget.item(self.queryBookResultTableWidget.currentRow(),
                                                                    0).text(), 30, self.date.split('/')[0],
                               self.date.split('/')[1], self.date.split('/')[2])
            print(sql)
            conn = pymysql.Connect(host='47.93.21.11', user="root", port=3306, password="lovemiss1314",
                                   database="tsglxt")
            cur = conn.cursor()

            length = cur.execute(sql)
            sql = """
                UPDATE books SET bCurNum=bCurNum-1 where  isbn='{}'
                """.format(self.queryBookResultTableWidget.item(self.queryBookResultTableWidget.currentRow(),
                                                                0).text())
            cur.execute(sql)
            sql = """
                UPDATE readers set rBorrowedNum=rBorrowedNum+1 where  borrowid='{}'
                """.format(self.currentUserid)

            cur.execute(sql)
            sql = """
                UPDATE readers set rCurNum=rCurNum-1 where borrowid='{}'
                """.format(self.currentUserid)
            cur.execute(sql)
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()

    def on_returnBtn_clicked(self):
        print("还书按钮被按下")
        if self.returnStatus == 0:
            self.queryBookResultTableWidget.clear()
            self.queryBookResultTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.queryBookResultTableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
            sql = """
                        SELECT borrowid, isbn, startDate, DATEDIFF( curdate(),rb.startDate) FROM rb WHERE borrowid='{}';
                        """.format(self.currentUserid)

            try:
                con = pymysql.connect(host='47.93.21.11', user="root", port=3306, password="lovemiss1314",
                                      database="tsglxt")
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
                    self.queryBookResultTableWidget.setColumnCount(col)
                    self.queryBookResultTableWidget.setRowCount(row)
                    a = 0
                    for i in self.Header[2]:
                        # print(i)
                        self.queryBookResultTableWidget.setHorizontalHeaderItem(a, QTableWidgetItem(str(i)))
                        a += 1
                    for i in range(0, row):
                        for j in range(0, col):
                            self.queryBookResultTableWidget.setItem(i, j, QTableWidgetItem(str(data[i][j])))
                self.returnStatus = 1
            except Exception as e:
                print(e)
            finally:
                cur.close()
                con.close()
        elif self.returnStatus == 1:
            print(self.queryBookResultTableWidget.currentRow())
            if self.queryBookResultTableWidget.currentRow() == -1:
                QMessageBox.warning(self, '错误', '请先选择要还的书籍!', QMessageBox.Ok)
                return
            else:
                borrowid = self.queryBookResultTableWidget.item(self.queryBookResultTableWidget.currentRow(), 0).text()
                isbn = self.queryBookResultTableWidget.item(self.queryBookResultTableWidget.currentRow(), 1).text()
                sql = """
                    DELETE FROM rb WHERE borrowid='{}' and isbn='{}'
                    """.format(borrowid, isbn)

                try:
                    con = pymysql.connect(host='47.93.21.11', user="root", port=3306, password="lovemiss1314",
                                          database="tsglxt")
                    cur = con.cursor()
                    res = cur.execute(sql)
                    if res == 1:
                        QMessageBox.information(self, '完成', '还书成功!', QMessageBox.Ok)
                        sql = """
                                        UPDATE books SET bCurNum=bCurNum+1 where  isbn='{}'
                                        """.format(
                            isbn)
                        cur.execute(sql)
                        sql = """
                            update readers set rBorrowedNum=rBorrowedNum+1 where  borrowid='{}'
                            """.format(self.currentUserid)

                        cur.execute(sql)
                        sql = """
                                update readers set rCurNum=rCurNum-1 where  borrowid='{}'
                                                   """.format(self.currentUserid)
                        cur.execute(sql)
                    con.commit()
                except  Exception as e:
                    print(e)
                finally:
                    cur.close()
                    con.close()
                    self.returnStatus = 0

            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindowWidget('123', 0)
    main.show()
    sys.exit(app.exec_())
