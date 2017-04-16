import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant

class RequestHistoryModel(QAbstractTableModel):
    def __init__(self, data, parent=None, *args):
        """
        data should contain a list of dicts for now
        """
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = data

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0].keys())

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()

        col = index.column()
        key = list(self.arraydata[index.row()].keys())[index.column()]

        return QVariant(self.arraydata[index.row()][key])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(list(self.arraydata[0].keys())[col])

        return QVariant()

    def sort(self, Ncol, order):
        """
        Sort table by given column number.
        """
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        self.emit(SIGNAL("layoutChanged()"))

class HPMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def _exitAction(self):
        smileyIcon = QIcon('icons/smiley.png')
        exitAction = QAction(smileyIcon, 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Smiley face will wreck your shit.')

        exitAction.triggered.connect(self.close)

        return exitAction

    def _initFakeModel(self):
        fakeRequest = {
            "id": "1",
            "host": "http://localhost",
            "method": "GET",
            "path": "/test/index.php",
            "response_status": "200",
            "length": "300",
            "title": "HOw to hax0r.",
        }

        fakeData = []
        for nb in range(35):
            fakeData.append(fakeRequest)

        return fakeData

    def initUI(self):
        centralWidget = QWidget()
        layout = QVBoxLayout()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        m = RequestHistoryModel(self._initFakeModel())
        tableView = QTableView()
        tableView.setSelectionBehavior(QTableView.SelectRows)
        tableView.setModel(m)
        layout.addWidget(tableView)
        layout.addWidget(QTextEdit())

        self.statusBar()
        self.setGeometry(300, 300, 1024, 768)
        self.setWindowTitle('Headphone HTTP Proxy')
        self.setWindowIcon(QIcon('icons/smiley.png'))
        self.initButtons()
        self.show()

    def initButtons(self):
        exitAction = self._exitAction()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('MainToolbar')
        toolbar.addAction(exitAction)

def init():
    app = QApplication(sys.argv)
    ex = HPMainWindow()
    sys.exit(app.exec_())
