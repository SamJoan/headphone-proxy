import sys
from PyQt5.QtWidgets import QMainWindow, QTableView, QAction, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant

class RequestHistoryModel(QAbstractTableModel):
    def __init__(self, datain, headerdata, parent=None, *args):
        """ datain: a list of lists
            headerdata: a list of strings
        """
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

    def sort(self, Ncol, order):
        """Sort table by given column number.
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

    def initUI(self):
        m = RequestHistoryModel([["a", "b", "c"]], ["colA","colB","colC"])
        tableView = QTableView()
        tableView.setModel(m)

        self.statusBar()
        self.setCentralWidget(tableView)
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
