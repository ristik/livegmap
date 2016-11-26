# -*- coding: utf-8 -*-
import os
import json
import logging

import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options

LOG = logging.getLogger(__name__)

WEBSOCKS = []
HISTORY = []

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect("/static/addr.html")

class MapHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect("/static/map.html")

class ApiHandler(tornado.web.RequestHandler):
    def post(self):
        result = {"success": False}
        x = self.get_argument("x")
        y = self.get_argument("y")
        name = self.get_argument("locality")
        if not (len(name) > 0 and len(x) > 0 and len(y) > 0):
            self.send_error(400)
            return

        num = 0
        data = {"lat": x, "lng": y, "title": name}
        data = json.dumps(data)
        for sock in WEBSOCKS:
            try:
                sock.write_message(data)
                num = num + 1
            except Exception:
                pass
        if num == 0:
            self.send_error(403)
            return

        HISTORY.append(data)
        LOG.info(data)
        result = {"success": True,
                  "message": "Salvestatud! %dx%d" % (num, len(HISTORY))}
        self.write(json.dumps(result))


class ReplayHandler(tornado.web.RequestHandler):

    def get(self, *args):
        self.write(json.dumps(HISTORY))


class ResetHandler(tornado.web.RequestHandler):

    def get(self, *args):
        global HISTORY
        HISTORY = []
        self.write("Puhas vuuk.")


class WebSocketBroadcaster(tornado.websocket.WebSocketHandler):
    """Keeps track of all websocket connections in
    the global WEBSOCKS variable.
    """
    def __init__(self, *args, **kwargs):
        super(WebSocketBroadcaster, self).__init__(*args, **kwargs)

    def open(self):
        LOG.info("Opened socket %r" % self)
        if self not in WEBSOCKS:
            WEBSOCKS.append(self)

    def on_message(self, message):
        LOG.info(u"Got message from websocket: %s" % message)

    def on_close(self):
        LOG.info("Closed socket %r" % self)
        if self in WEBSOCKS:
            WEBSOCKS.remove(self)


settings = {
    'static_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"),
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/map", MapHandler),
    (r"/api", ApiHandler),
    (r"/replay", ReplayHandler),
    (r"/reset", ResetHandler),
    (r"/sock", WebSocketBroadcaster)],
                                      **settings)


if __name__ == "__main__":
    define("port", default=80, help="Run server on a specific port", type=int)
    tornado.options.parse_command_line()

    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
