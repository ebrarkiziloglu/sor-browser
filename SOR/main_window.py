import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from SOR.browser import Browser

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Browser")
        self.setGeometry(100, 100, 1200, 800)

        self.browser = Browser()
        self.setCentralWidget(self.browser)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
