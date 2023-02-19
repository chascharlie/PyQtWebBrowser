from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QWidget 

from ui_output import Ui_Form
import sys

class MainWindow(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.backButton.clicked.connect(self.goBack)
        self.forwardButton.clicked.connect(self.goForward)
        self.refreshButton.clicked.connect(self.refresh)
        self.addressBar.returnPressed.connect(self.navigateUrl)
        
        self.webView.urlChanged.connect(self.updateUrl)
        self.webView.titleChanged.connect(self.updateTitle)

        self.webView.setUrl(QUrl("http://google.com"))

    def goBack(self):
        self.webView.back()

    def goForward(self):
        self.webView.forward()

    def refresh(self):
        self.webView.reload()

    def updateUrl(self,url):
        self.addressBar.setText(url.toString())

    def updateTitle(self,title):
        self.setWindowTitle(f"{title} - PyQtWebBrowser")

    def navigateUrl(self):
        url = self.addressBar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://"+url

        self.webView.setUrl(QUrl(url))

app = QApplication(sys.argv)
view = MainWindow()
view.show()
app.exec()