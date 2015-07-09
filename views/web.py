import views.interface
from flask import Flask
from flask import request
import webbrowser


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
            self.shutdown_server()
            self.started = False
            return "shutting down"

    def start(self):
        webbrowser.open("http://localhost:8080")
        self.app.run(host="localhost", port=8080, debug=True)

    def ask_user_for_config(self):
        print("ask for config!")

    def shutdown_server(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
