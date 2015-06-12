class Question(object):
    def __init__(self, to_ask, answer):
        self.to_ask = to_ask
        self.the_answer = answer

    def ask(self):
        return self.to_ask

    def answer(self, user_answer):
        return user_answer == self.the_answer
