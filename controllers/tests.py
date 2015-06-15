# -*- coding: utf-8 -*-
import unittest
import mock  # TODO make this import conditional for Python 3 compatibility
from controllers.vtestcontroller import VerbTestController
import lib.verbs as verbs
import lib.database as database
import lib.quiz as quiz
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

    def test_start(self):
        view = self.MockQuizView()
        controller = VerbTestController(view)

        view.request_quiz_config = mock.MagicMock()

        controller.start()

        args, _ = view.request_quiz_config.call_args
        self.assertEqual(view.request_quiz_config.call_count, 1)

        self.assertTrue(callable(args[0]),
                        "Controller did not provide view with valid callback")

    def test_full_quiz_cycle(self):
        ''' Arguably more a functional/integration test '''
        view = self.MockQuizView()
        controller = VerbTestController(view)

        number_of_questions = 10
        Inf = verbs.Inflections
        view.mock_config = {"number_of_questions": number_of_questions,
                            "inflections": {
                                Inf.PLAIN: [Inf.POLITE, Inf.NEGATIVE_POLITE]
                                }
                           }

        # Patch view.ask_question to just call the callback with a blank answer
        view.ask_question = mock.MagicMock(
            side_effect=lambda q, callback: callback(""))

        # Patch view.on_finish_quiz so we know it's called with the right data
        view.on_finish_quiz = mock.MagicMock()

        # Patching the controller metheod get_question so I can be sure of what
        # the answer is. Unsure if this is good practice...
        controller.get_question = lambda: quiz.Question(object, "Question",
                                                        lambda x: "")

        # Run the test
        controller.start()

        self.assertEqual(view.ask_question.call_count, number_of_questions,
                         "Did not ask {} questions".format(number_of_questions))

        # All answers should be correct - TODO make correct answers randomised
        self.assertEqual(view.on_finish_quiz.call_count, 1)

        self.assertFalse(True, "Finish the test")

    def test_build_questions(self):
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


    class MockQuizView(QuizView):
        def __init__(self):
            super(TestVerbTestController.MockQuizView, self).__init__()
            self.mock_config = None

        def do_request_config(self):
            self.set_quiz_config(self.mock_config)


if __name__ == "__main__":
    unittest.main()
