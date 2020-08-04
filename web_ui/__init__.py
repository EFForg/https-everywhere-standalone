from flask import Flask, render_template, request
import threading, json

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
    global rw
    rw = rewriter
    threading.Thread(target=app.run, kwargs={'port': port}).start()
