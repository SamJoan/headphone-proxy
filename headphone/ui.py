import sys
import socket
import zeroless
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *

REFRESH_INTERVAL = 100
IPC_PORT = 31337

class HPMainWindow(QMainWindow):
    """
    Displays a history of all requests seen by the proxy.
    """
    historyWidget = None

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

    def _initIPC(self):
        sock = socket.socket()
        sock.connect(('127.0.0.1', IPC_PORT))
        sock.setblocking(0)

        return sock

    def _updateHistory(self):
        try:
            if not self.ipc:
                self.ipc = zeroless.Server(port=IPC_PORT).pull()

        finally:
            QTimer.singleShot(REFRESH_INTERVAL, self._updateHistory)

    def _initFakeTable(self, tableWidget):
        fakeRequest = {
            "host": "http://localhost",
            "method": "GET",
            "path": "/test/index.php",
            "response_status": "200",
            "length": "300",
            "title": "HOw to hax0r.",
        }

        col_names = list(fakeRequest.keys())
        cols = len(col_names)
        rows = 300
        tableWidget.setRowCount(rows)
        tableWidget.setColumnCount(cols)
        tableWidget.setHorizontalHeaderLabels(col_names)
        tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        fakeData = []
        for row in range(300):
            for col in range(cols):
                key = list(fakeRequest.keys())[col]
                val = fakeRequest[key]

                tableWidget.setItem(row, col, QTableWidgetItem(val))

        return fakeData

    def _requestClicked(self, row, column):
        self.requestWidget.setText("""GET /test/index.php HTTP/1.1
Host: localhost

""")
        self.responseWidget.setText("""HTTP/1.1 200 OK
Content-type: text/html

OK, you got it
""")

    def _initHistory(self):
        historyWidget = QTableWidget(self)
        historyWidget.setSelectionBehavior(QTableView.SelectRows)
        historyWidget.cellClicked.connect(self._requestClicked)
        self._initFakeTable(historyWidget)

        return historyWidget

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

        self.historyWidget = self._initHistory()
        self.requestWidget, self.responseWidget = self._initDetailView()

        tabWidget = self._initTabs(self.requestWidget, self.responseWidget)

        layout.addWidget(self.historyWidget)
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
    ex = HPMainWindow()
    sys.exit(app.exec_())
