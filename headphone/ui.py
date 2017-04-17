import sys
import socket
import zeroless
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *

REFRESH_INTERVAL = 100
IPC_PORT = 31337

main_window = None

class RequestHistoryTable(QTableWidget):
    def initTable(self):
        col_names = ["Host", "Method", "Path", "Status code", "Length"]
        self.setHorizontalHeaderLabels(col_names)
        cols = len(col_names)

        self.setRowCount(0)
        self.setColumnCount(cols)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def addRequest(self, flow):
        request = flow.request
        nbRows = self.rowCount()

        self.insertRow(nbRows)
        self.setItem(nbRows, 0, QTableWidgetItem(request.host))
        self.setItem(nbRows, 1, QTableWidgetItem(request.method))
        self.setItem(nbRows, 2, QTableWidgetItem(request.path))
        self.setItem(nbRows, 3, QTableWidgetItem("wuhevs"))

    def updateRequest(self, flow):
        print("updateRequest: ", flow)

class HPMainWindow(QMainWindow):
    """
    Displays a history of all requests seen by the proxy.
    """
    history = None

    """
    Displays a raw HTTP request for an individual request that was clicked by the user.
    """
    requestWidget = None

    """
    Displays a raw HTTP response for an individual request that was clicked by the user.
    """
    responseWidget = None

    ipc = None

    def __init__(self):
        super().__init__()

        self.initUI()

    def _updateHistory(self):
        try:
            if not self.ipc:
                self.ipc = zeroless.Server(port=IPC_PORT).pull()

        finally:
            QTimer.singleShot(REFRESH_INTERVAL, self._updateHistory)

    def _requestClicked(self, row, column):
        self.requestWidget.setText("""GET /test/index.php HTTP/1.1
Host: localhost

""")
        self.responseWidget.setText("""HTTP/1.1 200 OK
Content-type: text/html

OK, you got it
""")

    def _initHistory(self):
        history = RequestHistoryTable(self)
        history.setSelectionBehavior(QTableView.SelectRows)
        history.cellClicked.connect(self._requestClicked)
        history.initTable()

        return history

    def _initDetailView(self):

        requestWidget = QTextEdit()
        requestWidget.setReadOnly(True)

        responseWidget = QTextEdit()
        responseWidget.setReadOnly(True)

        return requestWidget, responseWidget

    def _initTabs(self, requestWidget, responseWidget):
        tabsWidget = QTabWidget()
        tabsWidget.addTab(requestWidget, "Request")
        tabsWidget.addTab(responseWidget, "Response")

        return tabsWidget

    def initUI(self):
        centralWidget = QWidget()
        layout = QVBoxLayout()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        self.history = self._initHistory()
        self.requestWidget, self.responseWidget = self._initDetailView()

        tabWidget = self._initTabs(self.requestWidget, self.responseWidget)

        layout.addWidget(self.history)
        layout.addWidget(tabWidget)

        self.statusBar()
        self.setGeometry(300, 300, 1024, 768)
        self.setWindowTitle('Headphone HTTP Proxy')
        self.setWindowIcon(QIcon('icons/smiley.png'))
        self.initButtons()

        self._updateHistory()

        self.show()

    def initButtons(self):
        smileyIcon = QIcon('icons/smiley.png')

        exitAction = QAction(smileyIcon, 'Exit', self)
        exitAction.setStatusTip('Smiley face will wreck your shit.')
        exitAction.triggered.connect(self.close)

        justSmileAction = QAction(smileyIcon, 'Smile', self)
        justSmileAction.setStatusTip('Proxy now listening on port 8080.')

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        exitAction = QAction(smileyIcon, 'Exit', self)
        exitAction.setStatusTip('Smiley face will wreck your shit.')

        toolbar = self.addToolBar('MainToolbar')
        toolbar.addAction(justSmileAction)

def init():
    app = QApplication(sys.argv)
    main_window = HPMainWindow()

    return app, main_window
