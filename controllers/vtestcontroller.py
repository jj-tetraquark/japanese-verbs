# -*- coding: utf-8 -*-
import random
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
        predicate = self.quiz_inflections.keys()[0]
        # List comprehension to stop asking for itself
        possible_asks = [x for x in self.quiz_inflections[predicate]
                         if x != predicate]

        asking_for = random.choice(possible_asks)

        return {"data": verbs.Verb(**self.db.get_verb()),
                "asking_for": asking_for,
                "answer": lambda o: o.get_inflection(asking_for),
                "predicate": lambda o: o.get_inflection(predicate)
                }
