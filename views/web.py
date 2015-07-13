import views.interface
from flask import Flask
from flask import request
from time import sleep
import webbrowser
import multiprocessing
from ctypes import c_bool
import threading


class WebView(views.interface.QuizView):
    ''' Web browser based view '''

    def __init__(self):
        super(WebView, self).__init__()
        self.app = Flask(__name__)

        @self.app.route('/')
        def hello_world():
            return 'Hello World!'

        @self.app.route('/imready') # temporary
        def notify_started():
            self.started = True
            return 'Started'

        @self.app.route('/shutdown')
        def shutdown_server():
            self.keep_alive.value = False
            return "shutting down"

        self.keep_alive = multiprocessing.Value(c_bool, True)

        self.server = multiprocessing.Process(
            target=self.app.run, kwargs={"port":8080, "debug":False})

        self.server.start()
        self.server_thread = threading.Thread(target=self.server_process_loop)
        self.server_thread.start()

    def start(self):
        webbrowser.open("http://localhost:8080")

    def ask_user_for_config(self):
        print("ask for config!")

    def shutdown_server(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    def server_process_loop(self):
        while self.keep_alive.value:
            sleep(3)
        self.server.terminate()
        self.server.join()
