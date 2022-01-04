
import LoginWidget
import sys

from PyQt5.QtWidgets import *



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app=QApplication(sys.argv)
    main=LoginWidget.TsLogin()
    main.show()
    sys.exit(app.exec_())
