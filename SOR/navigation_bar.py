import re
from urllib.parse import urlparse
from PyQt5.QtWidgets import QAction, QToolBar, QLineEdit
from PyQt5.QtCore import QUrl, QSize, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView

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
        self.url_bar = QLineEdit('',self)
        self.url_bar.setPlaceholderText("sor will never follow you")
        self.url_bar.returnPressed.connect(self.navigate_to_url) # search the url bar when return pressed
        self.url_bar.setFixedHeight(24)  # Set the height of the URL bar
        self.browser.urlChanged.connect(self.update_urlbar) # updaate url bar when the page is updated
        self.addWidget(self.url_bar)

    def navigate_home(self):
        self.browser.setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        text = self.url_bar.text()
        url = self.get_url(text)
        self.browser.setUrl(url)    

    def get_url(self, text):
        # Check if the input is a valid URL
        parsed_url = urlparse(text)
        if parsed_url.scheme and parsed_url.netloc:
            return QUrl(text)
        elif '.' in text:  # Handle cases where user enters URL without scheme
            return QUrl(f"http://{text}")
        else:
            # Treat the input as a search query
            return QUrl(f"https://www.google.com/search?q={text.replace(' ', '+')}")
        
    def update_urlbar(self, q):
        if q.toString() == "https://www.google.com/":
            self.url_bar.setText("")
            self.url_bar.setPlaceholderText("sor will never follow you")
        else:
            self.url_bar.setText(q.toString())
            self.setup_url_message_timer()
            self.setup_delay_timer()


    def setup_delay_timer(self):
        self.delay_timer = QTimer(self)
        self.delay_timer.setSingleShot(True)
        self.delay_timer.timeout.connect(self.setup_url_revert_timer)
        self.delay_timer.start(2000)
        
    def open_bookmarks(self):
        print("Bookmarks button clicked")

    def setup_url_message_timer(self):
        self.url_message_timer = QTimer(self)
        self.url_message_timer.timeout.connect(self.display_url_message)
        self.url_message_timer.start(10000)
    
    def display_url_message(self):
        self.url_bar.setText("")
        self.url_bar.setPlaceholderText("sor will never follow you")
    
    def setup_url_revert_timer(self):
        self.url_revert_timer = QTimer(self)
        self.url_revert_timer.timeout.connect(self.revert_url_message)
        self.url_revert_timer.start(10000)
    
    def revert_url_message(self):
        current_url = self.browser.url().toString()
        self.url_bar.setText(current_url)

