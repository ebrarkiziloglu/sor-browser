from PyQt5.QtWidgets import QMainWindow
from browser import Browser
from navigation_bar import NavigationBar


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Browser")
        self.setGeometry(100, 100, 1200, 800)

        self.browser = Browser()
        self.setCentralWidget(self.browser)

        navigation_bar = NavigationBar(self.browser)
        self.addToolBar(navigation_bar)
        self.showMaximized()
