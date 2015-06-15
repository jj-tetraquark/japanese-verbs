# -*- coding: utf-8 -*-
import unittest
import random
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

        args = tuple(view.request_quiz_config.call_args)[0]
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

        correct_answers = random.randrange(0, number_of_questions)

        # Patch view.ask_question to just call the callback with either
        # "correct" or "wrong" depending on how many times it's been
        # asked and the number of correct answers
        def mock_answer_question(q, callback):
            times_called = view.ask_question.call_count
            answer = "correct" if times_called <= correct_answers else "wrong"
            callback(answer)

        view.ask_question = mock.MagicMock(
            side_effect=mock_answer_question)

        # Patch view.handle_answer_result
        view.handle_answer_result = mock.MagicMock(
            side_effect=lambda ans, callback: callback())

        # Patch view.on_finish_quiz so we know it's called with the right data
        view.on_finish_quiz = mock.MagicMock()

        # Patching the controller methed make_question so the question answer
        # is always "correct"
        controller.make_question = lambda i: {"data": object(),
                                              "question": "Question",
                                              "answer": lambda x: "correct"}

        # Run the test
        controller.start()

        self.assertEqual(view.ask_question.call_count, number_of_questions,
                         "Did not ask {} questions".format(number_of_questions))

        self.assertEqual(view.handle_answer_result.call_count,
                         number_of_questions)

        self.assertEqual(view.on_finish_quiz.call_count, 1)
        on_finish_args = tuple(view.on_finish_quiz.call_args)[0]
        self.assertEqual(on_finish_args[0].get("correct_answers", None),
                         correct_answers, "Controller reported wrong score")

    @unittest.skip("Not testing this at the moment")
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
