import headphone.ui
from threading import Thread
import tornado.ioloop
from mitmproxy import addons
from mitmproxy import log
from mitmproxy import master
import sys
from mitmproxy.addons import eventstore
from mitmproxy.addons import intercept
from mitmproxy.addons import termlog
from mitmproxy.addons import view
from mitmproxy.options import Options
from mitmproxy.proxy import ProxyServer, ProxyConfig
from mitmproxy import options

class HeadphoneMaster(master.Master):

    """
    The QT QMainWindow.
    """
    main_window = None

    def __init__(self, options, server, with_termlog=True):
        super().__init__(options, server)
        self.view = view.View()
        self.view.sig_view_add.connect(self._sig_view_add)
        self.view.sig_view_remove.connect(self._sig_view_remove)
        self.view.sig_view_update.connect(self._sig_view_update)

        self.addons.add(*addons.default_addons())
        self.addons.add(
            intercept.Intercept(),
            self.view,
        )

    def _sig_view_add(self, view, flow):
        self.main_window.history.add_flow(flow)

    def _sig_view_update(self, view, flow):
        self.main_window.history.update_flow(flow)

    def _sig_view_remove(self, view, flow):
        raise Exception('wuht why')

    def run(self):
        iol = tornado.ioloop.IOLoop.instance()
        iol.add_callback(self.start)
        # tornado.ioloop.PeriodicCallback(lambda: self.tick(timeout=0), 5).start()
        # t = Thread(target=lambda: iol.start()).start()

        app, self.main_window = headphone.ui.init()
        Thread(target=lambda: self.main_window.history.add_flow(None)).start()
        sys.exit(app.exec_())

def main():
    hpm = HeadphoneMaster({}, ProxyServer(ProxyConfig(options.Options(listen_port=8080))))
    hpm.run()
