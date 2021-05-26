import sys
from PyQt5.QtWidgets import QApplication, QFileDialog
from os.path import expanduser
from gui import chukyso

def main():
    app = QApplication(sys.argv)
    gui = chukyso()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()