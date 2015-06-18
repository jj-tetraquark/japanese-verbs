class Question(object):
    def __init__(self, data, asks, answer, predicate=None):
        self.data = data  # data object
        self.asks = asks  # for the view to interperate
        self.correct_answer = answer(data)
        if predicate:
            self.predicate = predicate(data)
        else:
            self.predicate = None

    @classmethod
    def from_dictionary(cls, qdict):
        return cls(qdict["data"],
                   qdict["asking_for"],
                   qdict["answer"],
                   qdict.get("predicate", None))

    def ask(self):
        return (self.asks, self.predicate)

    def answer(self, user_answer):
        if isinstance(self.correct_answer, tuple):
            return user_answer in self.correct_answer
        else:
            return user_answer == self.correct_answer


class Quiz(object):
    def __init__(self, number_of_questions, question_generator):
        self.number_of_questions = number_of_questions
        self.current_question = 0
        self.correct_answers = 0

        self.questions = list()
        for _ in range(0, number_of_questions):
            self.questions.append(Question.from_dictionary(
                                  question_generator()))

    def length(self):
        return self.number_of_questions

    def finished(self):
        return self.current_question == self.number_of_questions

    def ask_question(self):
        return self.questions[self.current_question]

    def answer_question(self, answer):
        question = self.questions[self.current_question]
        self.current_question += 1
        result = question.answer(answer)
        if result:
            self.correct_answers += 1

        return result

    def answered_correctly(self):
        return self.correct_answers

    def score(self):
        return float(self.correct_answers) / self.number_of_questions * 100
