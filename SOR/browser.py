from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class Browser(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setUrl(QUrl("https://www.google.com"))
