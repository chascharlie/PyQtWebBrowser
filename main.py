from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QWidget 
from PyQt6 import QtWebEngineWidgets

from dialog import *
from ui_output import Ui_Form
import sys, os, csv

class MainWindow(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        if not os.path.exists("settings.csv") or os.path.getsize("settings.csv") == 0:
            with open("settings.csv","w+") as write:
                writer = csv.writer(write)
                rows = [["Setting","Value"],["Homepage","https://google.com"],["SearchEngine","0"]]
                writer.writerows(rows)

        self.backButton.clicked.connect(self.goBack)
        self.forwardButton.clicked.connect(self.goForward)
        self.refreshButton.clicked.connect(self.refresh)
    
        self.addressBar.returnPressed.connect(self.navigateUrl)
        self.searchBar.returnPressed.connect(self.searchQuery)

        self.settingsButton.clicked.connect(self.settings)

        self.addTabButton.clicked.connect(self.newTab)
        self.closeTabButton.clicked.connect(self.closeTab)

        self.tabWidget.currentChanged.connect(self.changeTab)

        self.newTab()
    
    def newTab(self):
        self.tabWidget.addTab(QtWebEngineWidgets.QWebEngineView(),"New Tab")
        index = self.tabWidget.currentIndex()+1
        self.tabWidget.setCurrentIndex(index)
        self.tabWidget.currentWidget().urlChanged.connect(self.updateUrl)
        self.tabWidget.currentWidget().titleChanged.connect(self.updateTitle)

        with open("settings.csv","r") as read:
            reader = csv.reader(read,skipinitialspace=True)
            readerList = list(reader)
            self.tabWidget.currentWidget().setUrl(QUrl(readerList[1][1]))
            self.searchSelection.setCurrentIndex(int(readerList[2][1]))

    def closeTab(self):
        index = self.tabWidget.currentIndex()
        self.tabWidget.removeTab(index)
        self.tabWidget.setCurrentIndex(index-1)

        if self.tabWidget.count() == 0:
            self.newTab()        

    def changeTab(self):
        url = self.tabWidget.currentWidget().url()
        title = self.tabWidget.currentWidget().title()
        self.updateUrl(url)
        self.updateTitle(title)

    def goBack(self):
        self.tabWidget.currentWidget().back()

    def goForward(self):
        self.tabWidget.currentWidget().forward()

    def refresh(self):
        self.tabWidget.currentWidget().reload()

    def updateUrl(self,url):
        self.addressBar.setText(url.toString())

    def updateTitle(self,title):
        if len(title) > 75:
            title = title[0:72]
            title = title + "..."

        self.setWindowTitle(f"{title} - PyQtWebBrowser")

        if len(title) > 25:
            title = title[0:22]
            title = title + "..."

        index = self.tabWidget.currentIndex()
        self.tabWidget.setTabText(index,title)

    def navigateUrl(self):
        url = self.addressBar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://"+url

        self.tabWidget.currentWidget().setUrl(QUrl(url))

    def searchQuery(self):
        query = self.searchBar.text()
        index = self.searchSelection.currentIndex()
        
        if index == 0:
            url = "https://www.google.com/search?q="+(query.replace(" ","+"))

        elif index == 1:
            url = "https://www.bing.com/search?q="+(query.replace(" ","+"))

        elif index == 2:
            url = "https://search.yahoo.com/search?p="+(query.replace(" ","+"))

        elif index == 3:
            url = "https://duckduckgo.com/?q="+(query.replace(" ","+"))

        self.tabWidget.currentWidget().setUrl(QUrl(url))
        self.searchBar.clear()

    def settings(self):
        Settings().exec()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = MainWindow()
    view.show()
    app.exec()