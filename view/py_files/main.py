from view.py_files.pyMainWindow import Ui_MainWindow
import sys
from PySide.QtGui import *
from PySide.QtCore import *


class Window(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setupUi(self)

    def view_pages(self):
        self.stackedWidget.

def main():
    QCoreApplication.setApplicationName("DigiBaseSkypeWindows")
    QCoreApplication.setApplicationVersion("0.1")
    QCoreApplication.setOrganizationName("DigiBaseReclass")
    QCoreApplication.setOrganizationDomain("DigiBaseReclass.com")




    app = QApplication(sys.argv)


    form = Window()
    form.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()