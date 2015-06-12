class Question(object):
    def __init__(self, to_ask, answer):
        self.to_ask = to_ask
        self.the_answer = answer

    @classmethod
    def from_tuple(cls, question_answer):
        return cls(question_answer[0], question_answer[1])

    def ask(self):
        return self.to_ask

    def answer(self, user_answer):
        return user_answer == self.the_answer


class Quiz(object):
    def __init__(self, number_of_questions, question_generator):
        self.questions = list()
        for _ in range(0, number_of_questions):
            self.questions.append(Question.from_tuple(question_generator()))

    def length(self):
        return len(self.questions)
