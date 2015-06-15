# -*- coding: utf-8 -*-
import lib.database as database
import lib.quiz as quiz
import lib.verbs as verbs


class VerbTestController(object):

    def __init__(self, view):
        # probably should make db configurable
        self.db = database.Database(database.DEFAULT_DATABASE_PATH)
        self.view = view
        self.quiz = None
        self.quiz_inflections = dict()

    def start(self):
        self.view.request_quiz_config(self.on_have_quiz_config)

    def on_have_quiz_config(self, config):
        self.new_quiz(config["number_of_questions"], config["inflections"])

    def new_quiz(self, number_of_questions, inflections):
        self.quiz_inflections = inflections
        self.quiz = quiz.Quiz(number_of_questions, self.make_question)
        self.maybe_ask_question()

    def maybe_ask_question(self):
        if not self.quiz.finished():
            self.view.ask_question(self.quiz.ask_question(),
                                   self.handle_answer)
        else:
            self.view.on_finish_quiz({"correct_answers":
                                      self.quiz.answered_correctly()})

    def handle_answer(self, answer):
        result = self.quiz.answer_question(answer)
        self.view.handle_answer_result(result, self.maybe_ask_question)

    def make_question(self):
        return {"data": verbs.Verb(**self.db.get_verb()),
                "asking_for": verbs.Inflections.POLITE,
                "answer": lambda o: o.masu(),
                "predicate": lambda o: o.plain()
                }
