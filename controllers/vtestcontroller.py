# -*- coding: utf-8 -*-
import lib.database as database
import lib.quiz as quiz
import lib.verbs as verbs


class VerbTestController(object):

    def __init__(self, view):
        # probably should make db configurable
        self.db = database.Database(database.DEFAULT_DATABASE_PATH)
        self.view = view

    def start(self):
        self.view.request_quiz_config(self.on_have_quiz_config)

    def on_have_quiz_config(config):
        pass  # something with new_quiz

    def new_quiz(self, number_of_questions, config):
        pass

    def get_question(self):
        verb = verbs.Verb(**self.db.get_verb())
        return quiz.Question(verb,
                             verbs.Inflections.POLITE,
                             lambda v: v.masu(),
                             lambda v: v.plain())
