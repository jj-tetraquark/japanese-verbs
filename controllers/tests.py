# -*- coding: utf-8 -*-
import unittest
import mock
from controllers.vtestcontroller import VerbTestController
import lib.verbs as verbs
import lib.database as database
from views.interface import QuizView


#TODO - Make this test run with mock data
@unittest.skipIf(
    not database.is_initialized(database.DEFAULT_DATABASE_PATH),
    "Database not initialized, need install before running this suite")
class TestVerbTestController(unittest.TestCase):

    def test_construction(self):
        ''' temporary test just to make sure that this all works'''
        controller = VerbTestController(QuizView())
        self.assertIsNotNone(controller)

    def test_full_quiz_cycle(self):
        view = QuizView()
        controller = VerbTestController(view)

        view.do_request_config = mock.MagicMock()
        controller.start()
        self.assertEqual(view.do_request_config.call_count, 1)

        self.assertFalse(True, "Finish the test")

    def test_create_quiz(self):
        controller = VerbTestController(QuizView())

        Inf = verbs.Inflections
        controller.new_quiz(10,  # number of questions
                            {
                                Inf.PLAIN:
                                [Inf.POLITE, Inf.NEGATIVE_POLITE]
                            })

        question = controller.get_question()

        self.assertTrue(question.ask()[0] is Inf.POLITE or
                        question.ask()[0] is Inf.NEGATIVE_POLITE)

        found_u = False
        # bit of a stretch but all plain form verbs should end in u
        for u in [u"う", u"つ", u"す", u"む", u"く", u"ぐ", u"ぬ", u"ぶ", u"る"]:
            if u in question.ask()[1]:
                found_u = True
                break

        self.assertTrue(found_u, "No plain verb found in question")

        self.assertTrue(False, "Finish the goddamn test!")


if __name__ == "__main__":
    unittest.main()
