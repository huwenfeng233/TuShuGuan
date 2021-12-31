import pymysql
import random
import randomName


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    con = pymysql.connect(host='47.93.21.11', user="root", port=3306, password="lovemiss1314", database="tsglxt")
    su = con.cursor()
    # for i in range(100):
    #     s = random.sample('zyxwvutsrqponmlkjihgfedcba',5)
    #     passwd=random.sample('zyxwvutsrqponmlkjihgfedcba',4)
    #     id=i;
    #     sql='INSERT INTO users VALUES (account="123123",passward="123456",id="asda")'
    #     try:
    #         su.execute(sql)
    #         con.commit()
    #         # con.submit()
    #     except Exception as e:
    #         print(e)
    #         con.rollback()
    # su.execute("""INSERT INTO users values ('王','军','明')""")
    # con.commit()
    sql = 'SELECT * FROM users'
    res = su.execute(sql)
    print(su.fetchall(), sep=' ')

    # for item in range(res):
    #     print (su.fetchone())
    con.close()
    su.close()

    # print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
