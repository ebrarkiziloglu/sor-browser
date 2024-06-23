from PyQt5.QtWidgets import QAction, QToolBar, QLineEdit
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtGui import QIcon

class NavigationBar(QToolBar):

    def __init__(self, *args, **kwargs):
        super(NavigationBar, self).__init__(*args, **kwargs)
        self.browser = args[0]

        # Set the height of the toolbar
        self.setFixedHeight(50)

        # Set the size of the icons
        self.setIconSize(QSize(16, 16))

        # back button with custom icon
        back_button = QAction(QIcon('icons/left-arrow.png'), 'Back', self)
        back_button.triggered.connect(self.browser.back)
        self.addAction(back_button)

        # forward button with custom icon
        forward_button = QAction(QIcon('icons/right-arrow.png'), 'Forward', self)
        forward_button.triggered.connect(self.browser.forward)
        self.addAction(forward_button)

        # reload button with custom icon
        reload_button = QAction(QIcon('icons/sync.png'), 'Reload', self)
        reload_button.triggered.connect(self.browser.reload)
        self.addAction(reload_button)

        # home button with custom icon
        home_button = QAction(QIcon('icons/home.png'), 'Home', self)
        home_button.triggered.connect(self.navigate_home)
        self.addAction(home_button)

        # bookmarks button with custom icon
        bookmarks_button = QAction(QIcon('icons/bookmark.png'), 'Bookmarks', self)
        bookmarks_button.triggered.connect(self.open_bookmarks)
        self.addAction(bookmarks_button)

        # URL bar
        url_bar = QLineEdit('Sor will never follow you...',self)
        url_bar.setFixedHeight(24)  # Set the height of the URL bar
        self.addWidget(url_bar)

    def navigate_home(self):
        self.browser.setUrl(QUrl("http://www.google.com"))

    def open_bookmarks(self):
        print("Bookmarks button clicked")
