class QuizView(object):
    ''' This defines the interface and some base class methods
        for a standard view. I appreciate doing it this way isn't
        especially Pythonic and I may remove this later if it seems
        necessary, but let me think C++ for now, kay? '''

    def __init__(self):
        self.set_config_callback = None
        self.answer_question_callback = None

    def init_splash(self):
        ''' Initial view setup. Normally called by __init__ but can be called
            manually '''
        raise NotImplementedError("Init splash not implemented")

    def request_quiz_config(self, callback):
        ''' Requests the quiz config from the user. Takes callback for when
            done '''
        self.set_config_callback = callback
        self.do_request_config()

    def do_request_config(self):
        ''' Actually does the UI for requesting the config '''
        raise NotImplementedError("do_request_config not implemented")

    def set_quiz_config(self, config):
        ''' Sets the quiz config through the callback '''
        if callable(self.set_config_callback):
            self.set_config_callback(config)
            self.set_config_callback = None  # expire!
        else:
            raise RuntimeError("Set config callback invalid")

    def ask_question(self, question, callback):
        ''' Requests the view to ask the user a question  and stores the
            callback'''
        self.answer_question_callback = callback
        self.do_ask_question(question)

    def do_ask_question(self, question):
        ''' Actually does the UI for asking the user a question '''
        raise NotImplementedError("do_ask_question not implemented")

    def submit_answer(self, answer):
        ''' Send the answer back to the controller via the callback '''
        if callable(self.answer_question_callback):
            self.answer_question_callback(answer)
            self.answer_question_callback = None
        else:
            raise RuntimeError("Answer question callback invalid")

    def on_finish_quiz(self, data):
        ''' Display the score and give option to restart or something '''
        raise NotImplementedError("on_finish_quiz not implemented")
