import views.interface
from flask import Flask
import webbrowser


class WebView(views.interface.QuizView):
    ''' Web browser based view '''

    def __init__(self):
        super(WebView, self).__init__()
        self.app = Flask(__name__)

        @self.app.route('/')
        def hello_world():
            return 'Hello World!'

    def init_splash(self):
        webbrowser.open("http://localhost:8080")
        self.app.run(host="localhost", port=8080, debug=True)

    def ask_user_for_config(self):
        pass
