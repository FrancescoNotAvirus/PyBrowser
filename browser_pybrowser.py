import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings


# ✅ Google versione leggera
HOME_URL = "https://www.google.com/search?igu=1&hl=en&pws=0&nfpr=1"


class BrowserTab(QtWidgets.QWidget):
    def __init__(self, url):
        super().__init__()

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.web = QWebEngineView()
        self.web.setUrl(QUrl(url))
        self.web.setZoomFactor(1.0)


        settings = self.web.settings()

        self.web.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )

        layout.addWidget(self.web)


class Browser(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyBrowser")
        self.resize(1400, 900)

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)

        self.layout = QtWidgets.QVBoxLayout(central)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.setDocumentMode(True)

        self.layout.addWidget(self.tabs)

        self.setup_profile()
        self.build_ui()

        self.add_tab(HOME_URL)

    def setup_profile(self):
        profile = QWebEngineProfile.defaultProfile()

        # 💀 User-Agent vecchissimo → Google diventa minimale
        profile.setHttpUserAgent(
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36"

        )

    def build_ui(self):
        nav = QtWidgets.QToolBar()
        nav.setMovable(False)
        nav.setFixedHeight(42)
        nav.setIconSize(QtCore.QSize(18, 18))
        self.addToolBar(nav)

        style = self.style()

        back = QtWidgets.QAction(style.standardIcon(QtWidgets.QStyle.SP_ArrowBack), "", self)
        back.triggered.connect(lambda: self.safe(lambda t: t.web.back()))
        nav.addAction(back)

        forward = QtWidgets.QAction(style.standardIcon(QtWidgets.QStyle.SP_ArrowForward), "", self)
        forward.triggered.connect(lambda: self.safe(lambda t: t.web.forward()))
        nav.addAction(forward)

        reload = QtWidgets.QAction(style.standardIcon(QtWidgets.QStyle.SP_BrowserReload), "", self)
        reload.triggered.connect(lambda: self.safe(lambda t: t.web.reload()))
        nav.addAction(reload)

        home = QtWidgets.QAction(style.standardIcon(QtWidgets.QStyle.SP_DirHomeIcon), "", self)
        home.triggered.connect(self.go_home)
        nav.addAction(home)

        newtab = QtWidgets.QAction(style.standardIcon(QtWidgets.QStyle.SP_FileDialogNewFolder), "", self)
        newtab.triggered.connect(lambda: self.add_tab(HOME_URL))
        nav.addAction(newtab)

        self.urlbar = QtWidgets.QLineEdit()
        self.urlbar.setPlaceholderText("Search or enter URL...")
        self.urlbar.returnPressed.connect(self.load_url)
        nav.addWidget(self.urlbar)

        self.tabs.currentChanged.connect(self.update_url)

    def current(self):
        return self.tabs.currentWidget()

    def safe(self, func):
        tab = self.current()
        if tab:
            func(tab)

    def add_tab(self, url):
        tab = BrowserTab(url)
        i = self.tabs.addTab(tab, "New Tab")
        self.tabs.setCurrentIndex(i)

        tab.web.urlChanged.connect(lambda q, t=tab: self.sync_url(q, t))
        self.update_url()

    def close_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def load_url(self):
        url = self.urlbar.text().strip()
        if not url:
            return

        if not url.startswith("http"):
            url = "https://" + url

        self.safe(lambda t: t.web.setUrl(QUrl(url)))

    def go_home(self):
        self.safe(lambda t: t.web.setUrl(QUrl(HOME_URL)))

    def sync_url(self, q, tab):
        if tab == self.current():
            self.urlbar.setText(q.toString())

    def update_url(self):
        tab = self.current()
        if tab:
            self.urlbar.setText(tab.web.url().toString())


app = QtWidgets.QApplication(sys.argv)
w = Browser()
w.show()
sys.exit(app.exec_())