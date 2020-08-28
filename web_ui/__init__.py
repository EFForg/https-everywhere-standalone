from flask import Flask, render_template, request
from werkzeug.serving import make_server
import threading, json, logging


class ServerThread(threading.Thread):

    def __init__(self, app, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.srv = make_server(str(host), port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        print(f"Starting Web UI on http://{str(self.host)}:{str(self.port)}")
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()


app = Flask(__name__)

@app.route('/')
def index():
    settings = rw.settings()

    return render_template('index.html',
                           ease=settings['ease'],
                           enabled=settings['enabled'],
                           update_channel_timestamps=json.dumps(settings['update_channel_timestamps']),
                           sites_disabled=json.dumps(list(settings['sites_disabled'])),
                           version_string=settings['version_string'])

@app.route('/settings_changed', methods=['POST'])
def settings_changed():
    results = json.loads(request.data)
    rw.update(results)
    return results.__repr__()

@app.route('/set_site_disabled', methods=['POST'])
def set_site_disabled():
    results = json.loads(request.data)
    return json.dumps(rw.set_site_disabled(results['site'], results['disabled']))


def run(host, port, rewriter):
    global rw, server
    rw = rewriter

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    server = ServerThread(app, host, port)
    server.start()

def shutdown():
    global server
    server.shutdown()
