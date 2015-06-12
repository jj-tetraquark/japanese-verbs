class Question(object):
    def __init__(self, to_ask, answer):
        self.to_ask = to_ask
        self.correct_answer = answer

    @classmethod
    def from_tuple(cls, question_answer):
        return cls(question_answer[0], question_answer[1])

    def ask(self):
        return self.to_ask

    def answer(self, user_answer):
        return user_answer == self.correct_answer


class Quiz(object):
    def __init__(self, number_of_questions, question_generator):
        self.number_of_questions = number_of_questions
        self.current_question = 0
        self.correct_answers = 0

        self.questions = list()
        for _ in range(0, number_of_questions):
            self.questions.append(Question.from_tuple(question_generator()))

    def length(self):
        return self.number_of_questions

    def finished(self):
        return self.current_question == self.number_of_questions

    def ask_question(self):
        return self.questions[self.current_question].ask()

    class Result:
        def __init__(self, correct, actual_answer):
            self.correct = correct
            self.correct_answer = actual_answer

    def answer_question(self, answer):
        question = self.questions[self.current_question]
        self.current_question += 1
        result = self.Result(question.answer(answer), question.correct_answer)
        if result.correct:
            self.correct_answers += 1

        return result

    def answered_correctly(self):
        return self.correct_answers

    def score(self):
        return float(self.correct_answers) / self.number_of_questions * 100
