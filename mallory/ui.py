import sys
from PyQt5.QtWidgets import QMainWindow, QTableView, QAction, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QAbstractTableModel

class RequestHistoryModel(QAbstractTableModel):
    def rowCount(self, _):
        return 1

    def columnCount(self, _):
        return 5

    def data(self, _, a):
        return [
            ("http:/google.com", "GET", "/admin", "a", "aa")
        ]

class HPMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        tableView = QTableView()
        tableView.setModel(RequestHistoryModel())
        self.setCentralWidget(tableView)

        smileyIcon = QIcon('icons/smiley.png')
        exitAction = QAction(smileyIcon, 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Smiley face will wreck your shit.')
        exitAction.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Headphone HTTP Proxy')
        self.show()

        self.setWindowIcon(smileyIcon)

def init():
    app = QApplication(sys.argv)
    ex = HPMainWindow()
    sys.exit(app.exec_())
