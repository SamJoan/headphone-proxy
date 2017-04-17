import headphone.ui
import tornado.ioloop
from mitmproxy import addons
from mitmproxy import log
from mitmproxy import master
from mitmproxy.addons import eventstore
from mitmproxy.addons import intercept
from mitmproxy.addons import termlog
from mitmproxy.addons import view
from mitmproxy.options import Options
from mitmproxy.tools.web import app
from mitmproxy.proxy import ProxyServer, ProxyConfig
from mitmproxy import options

class HeadphoneMaster(master.Master):
    def __init__(self, options, server, with_termlog=True):
        super().__init__(options, server)
        self.view = view.View()
        self.view.sig_view_add.connect(self._sig_view_add)
        self.view.sig_view_remove.connect(self._sig_view_remove)
        self.view.sig_view_update.connect(self._sig_view_update)
        self.view.sig_view_refresh.connect(self._sig_view_refresh)

        self.events = eventstore.EventStore()
        self.events.sig_add.connect(self._sig_events_add)
        self.events.sig_refresh.connect(self._sig_events_refresh)

        self.options.changed.connect(self._sig_options_update)

        self.addons.add(*addons.default_addons())
        self.addons.add(
            intercept.Intercept(),
            self.view,
            self.events,
        )
        if with_termlog:
            self.addons.add(termlog.TermLog())
        self.app = app.Application(
            self, self.options.web_debug
        )
        # This line is just for type hinting
        self.options = self.options  # type: Options

    def _sig_view_add(self, view, flow):
        app.ClientConnection.broadcast(
            resource="flows",
            cmd="add",
            data=app.flow_to_json(flow)
        )

    def _sig_view_update(self, view, flow):
        app.ClientConnection.broadcast(
            resource="flows",
            cmd="update",
            data=app.flow_to_json(flow)
        )

    def _sig_view_remove(self, view, flow):
        app.ClientConnection.broadcast(
            resource="flows",
            cmd="remove",
            data=flow.id
        )

    def _sig_view_refresh(self, view):
        app.ClientConnection.broadcast(
            resource="flows",
            cmd="reset"
        )

    def _sig_events_add(self, event_store, entry: log.LogEntry):
        app.ClientConnection.broadcast(
            resource="events",
            cmd="add",
            data=app.logentry_to_json(entry)
        )

    def _sig_events_refresh(self, event_store):
        app.ClientConnection.broadcast(
            resource="events",
            cmd="reset"
        )

    def _sig_options_update(self, options, updated):
        app.ClientConnection.broadcast(
            resource="settings",
            cmd="update",
            data={k: getattr(options, k) for k in updated}
        )

    def init_tornado(self):
        try:
            iol.start()
        except KeyboardInterrupt:
            self.shutdown()

    def run(self):

        from threading import Thread

        iol = tornado.ioloop.IOLoop.instance()
        iol.add_callback(self.start)
        tornado.ioloop.PeriodicCallback(lambda: self.tick(timeout=0), 5).start()

        t = Thread(target=lambda: iol.start()).start()
        # t.start()

        headphone.ui.init()

        # t.join()

        # self.add_log(
        #     "Proxy server listening at http://{}:{}/".format(self.server.address[0], self.server.address[1]),
        #     "info"
        # )
        #
        # web_url = "http://{}:{}/".format(self.options.web_iface, self.options.web_port)
        # self.add_log(
        #     "Web   server listening at {}".format(web_url),
        #     "info"
        # )

        # if self.options.web_open_browser:
        #     success = open_browser(web_url)
        #     if not success:
        #         self.add_log(
        #             "No web browser found. Please open a browser and point it to {}".format(web_url),
        #             "info"
        #         )


def main():
    hpm = HeadphoneMaster({}, ProxyServer(ProxyConfig(options.Options(listen_port=8080))))
    hpm.run()
    # mallory.ui.init()
