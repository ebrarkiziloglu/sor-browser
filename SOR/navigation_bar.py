from PyQt5.QtWidgets import QAction, QToolBar, QLineEdit, QHBoxLayout, QWidget, QVBoxLayout, QLabel, QDialog, QPushButton, QListWidget, QToolTip
from PyQt5.QtCore import QUrl, QSize, QTimer, Qt, QPoint
from PyQt5.QtGui import QIcon
from urllib.parse import urlparse

from PyQt5.QtWebEngineWidgets import QWebEngineView

class NavigationBar(QToolBar):

    def __init__(self, *args, **kwargs):
        super(NavigationBar, self).__init__(*args, **kwargs)
        self.browser = args[0]

        # Initialize bookmarks list
        self.bookmarks = []

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
        self.url_bar = QLineEdit('', self)
        self.url_bar.setPlaceholderText("sor will never follow you")
        self.url_bar.returnPressed.connect(self.navigate_to_url)  # search the url bar when return pressed
        self.url_bar.setFixedHeight(24)  # Set the height of the URL bar
        self.browser.urlChanged.connect(self.update_urlbar)  # update url bar when the page is updated
        self.url_bar.setFixedWidth(1300)  # Set the width of the URL bar
        self.url_bar.setAlignment(Qt.AlignCenter)  # Center align the URL text initially
        self.url_bar.focusInEvent = self.focus_in_event  # Override focus in event
        self.url_bar.focusOutEvent = self.focus_out_event  # Override focus out event

        # Add bookmark icon to the URL bar
        self.bookmark_action = QAction(QIcon('icons/addbookmarks.png'), '', self)
        self.bookmark_action.triggered.connect(self.add_bookmark)
        self.url_bar.addAction(self.bookmark_action, QLineEdit.TrailingPosition)

        self.addWidget(self.url_bar)

    def navigate_home(self):
        self.browser.setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        text = self.url_bar.text()
        url = self.get_url(text)
        self.browser.setUrl(url)
        self.url_bar.clearFocus()  # Clear focus after navigating to the URL

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
        # Create and show the bookmarks dialog
        dialog = QDialog()
        dialog.setWindowTitle("Bookmarks")

        layout = QVBoxLayout()
        list_widget = QListWidget()

        for bookmark in self.bookmarks:
            list_widget.addItem(bookmark)

        layout.addWidget(list_widget)
        dialog.setLayout(layout)
        dialog.exec_()

    def add_bookmark(self):
        current_url = self.browser.url().toString()
        if current_url not in self.bookmarks:
            self.bookmarks.append(current_url)
            tooltip_text = f"Added {current_url} to bookmarks."
        else:
            tooltip_text = f"{current_url} is already in bookmarks."

        bookmark_pos = self.url_bar.mapToGlobal(self.url_bar.rect().bottomRight())
        QToolTip.showText(bookmark_pos, tooltip_text, self.url_bar)

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

    def focus_in_event(self, event):
        self.url_bar.setAlignment(Qt.AlignLeft)  # Align text to the left when focused
        super(QLineEdit, self.url_bar).focusInEvent(event)

    def focus_out_event(self, event):
        self.url_bar.setAlignment(Qt.AlignCenter)  # Align text to the center when not focused
        super(QLineEdit, self.url_bar).focusOutEvent(event)
