from flask import Flask, render_template, request
from werkzeug.serving import make_server
import threading, json, logging


class ServerThread(threading.Thread):

    def __init__(self, app, port):
        threading.Thread.__init__(self)
        self.port = port
        self.srv = make_server('127.0.0.1', port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        print('Starting Web UI on http://127.0.0.1:' + str(self.port))
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()


app = Flask(__name__)

@app.route('/')
def index():
    settings = rw.settings()
    return render_template('index.html',
                           ease=settings['ease'],
                           enabled=settings['enabled'])

@app.route('/settings_changed', methods=['POST'])
def settings_changed():
    results = json.loads(request.data)
    rw.update(results)
    return results.__repr__()


def run(port, rewriter):
    global rw, server
    rw = rewriter

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    server = ServerThread(app, port)
    server.start()

def shutdown():
    global server
    server.shutdown()
