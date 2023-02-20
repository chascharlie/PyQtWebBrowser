from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
import csv 

class Settings(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")
        self.setFixedSize(400,200)
        
        self.verticalLayout = QVBoxLayout()

        self.homepageRow = QHBoxLayout()
        self.homepageLabel = QLabel("Homepage")
        self.homepageEntry = QLineEdit()
        self.homepageRow.addWidget(self.homepageLabel)
        self.homepageRow.addWidget(self.homepageEntry)
        self.verticalLayout.addLayout(self.homepageRow)
        
        self.searchRow = QHBoxLayout()
        self.searchLabel = QLabel("Search Engine")
        self.searchCombo = QComboBox()
        self.searchCombo.addItem(QIcon("Graphics/google.png"), "Google")
        self.searchCombo.addItem(QIcon("Graphics/bing.png"), "Bing")
        self.searchCombo.addItem(QIcon("Graphics/yahoo.png"), "Yahoo")
        self.searchCombo.addItem(QIcon("Graphics/duckduckgo.png"), "DuckDuckGo")
        self.searchRow.addWidget(self.searchLabel)
        self.searchRow.addWidget(self.searchCombo)
        self.verticalLayout.addLayout(self.searchRow)
       
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacer)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.verticalLayout.addWidget(self.buttonBox)
        self.setLayout(self.verticalLayout)

        with open("settings.csv","r") as read:
            reader = csv.reader(read,skipinitialspace=True)
            readerList = list(reader)
            self.homepageEntry.setText(readerList[1][1])
            self.searchCombo.setCurrentIndex(int(readerList[2][1]))
            
        self.buttonBox.accepted.connect(self.saveSettings)
        self.buttonBox.rejected.connect(lambda: self.close())

    def saveSettings(self):
        with open("settings.csv","r") as read:
            reader = csv.reader(read,skipinitialspace=True)
            readerList = list(reader)

        readerList[1][1] = self.homepageEntry.text()
        readerList[2][1] = str(self.searchCombo.currentIndex())

        with open("settings.csv","w") as write:
            writer = csv.writer(write)
            writer.writerows(readerList)

        self.close()