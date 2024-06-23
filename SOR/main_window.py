import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from browser import Browser
from navigation_bar import NavigationBar


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sor Browser")
        self.setGeometry(100, 100, 1200, 800)

        self.browser = Browser()
        self.setCentralWidget(self.browser)

        navigation_bar = NavigationBar(self.browser)
        self.addToolBar(navigation_bar)
        self.showMaximized()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
