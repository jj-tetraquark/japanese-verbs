# -*- coding: utf-8 -*-
import lib.database as db
import lib.quiz as quiz


class VerbTestController(object):

    def __init__(self):
        # probably should make db configurable
        self.db = db.Database(db.DEFAULT_DATABASE_PATH)

    def new_quiz(self, number_of_questions, config):
        pass

    def get_question(self):
        return quiz.Question(u"会う", u"会います").ask()
