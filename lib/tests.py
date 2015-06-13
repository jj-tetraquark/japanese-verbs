#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import lib.database as database
import lib.verbs as verbs
from lib.verbs import Verb
from lib.quiz import Question
from lib.quiz import Quiz


@unittest.skipIf(
    not database.is_initialized(database.DEFAULT_DATABASE_PATH),
    "Database not initialized, need install before running this suite")
class TestDatabaseConnections(unittest.TestCase):

    def setUp(self):
        self.db = database.Database(database.DEFAULT_DATABASE_PATH)

    def test_get_random_verb(self):
        verb = self.db.get_verb()
        self.assertNotEqual(verb["kana"], "")  # kana should never be empty

    def test_get_all_verb_types(self):
        for v_type in verbs.Types.All():
            verb = self.db.get_verb(type=v_type)
            self.assertEqual(verb["type"], v_type)


class TestQuiz(unittest.TestCase):
    def test_question_class(self):
        the_question = "What is the answer to this question"
        the_answer = "the answer of course"

        question = Question(the_question, the_answer)
        self.assertEqual(question.ask(), the_question)
        self.assertFalse(question.answer("not the answer"))
        self.assertTrue(question.answer(the_answer))

    def test_quiz_construction(self):
        ''' should be constructed with a number of questions and a function
            that returns a question-answer tuple '''

        # Create a quiz with 10 questions
        quiz = Quiz(10, lambda: tuple(["The question", "The answer"]))
        self.assertEqual(quiz.length(), 10)

    def test_quiz_answering_and_grading(self):

        # using nonlocal here would be better, but python 2.7
        number_of_times_called = [0]

        def question_generator():
            number_of_times_called[0] += 1
            return tuple(["Question {}?".format(number_of_times_called[0]),
                          ("yes" if number_of_times_called[0] % 2 == 0
                              else "no")])

        test_quiz = Quiz(10, question_generator)

        question_number = 1
        while not test_quiz.finished():
            self.assertEqual("Question {}?".format(question_number),
                             test_quiz.ask_question())
            result = test_quiz.answer_question("yes")

            # this is testing the return type of result
            if result.correct:
                self.assertEqual(result.correct_answer, "yes")
            else:
                self.assertEqual(result.correct_answer, "no")

            question_number += 1

        self.assertEqual(test_quiz.answered_correctly(), 5)
        self.assertEqual(test_quiz.score(), 50.0)


class TestVerbClass(unittest.TestCase):
    ''' Common setup in this class, proper tests below'''
    def setUp(self):
        # declare verbs for use in the tests
        self.au = Verb(kana=u"あう", kanji=u"会う",
                       type=verbs.Types.GODAN, ending="u",
                       english="to meet")

        self.segamu = Verb(kana=u"せがむ",
                           type=verbs.Types.GODAN, ending="mu")

        self.taberu = Verb(kana=u"たべる", kanji=u"食べる",
                           type=verbs.Types.ICHIDAN, ending="ru")

        self.matsu = Verb(kana=u"まつ", kanji=u"待つ",
                          type=verbs.Types.GODAN, ending="tsu",
                          english="to wait")

        self.osu = Verb(kana=u"おす", kanji=u"押す",
                        type=verbs.Types.GODAN, ending="su",
                        english="to push, to press")

        self.nomu = Verb(kana=u"のむ", kanji=u"飲む",
                         type=verbs.Types.GODAN, ending="mu",
                         english="to drink, to swallow")

        self.hiku = Verb(kana=u"ひく", kanji=u"弾く",
                         type=verbs.Types.GODAN, ending="ku",
                         english="to play(piano or guitar)")

        self.oyogu = Verb(kana=u"およぐ", kanji=u"泳ぐ",
                          type=verbs.Types.GODAN, ending="gu",
                          english="to swim")

        self.shinu = Verb(kana=u"しぬ", kanji=u"死ぬ",
                          type=verbs.Types.GODAN, ending="nu",
                          english="to die")

        self.asobu = Verb(kana=u"あそぶ", kanji=u"遊ぶ",
                          type=verbs.Types.GODAN, ending="bu",
                          english="to play")

        self.kaeru = Verb(kana=u"かえる", kanji=u"帰る",
                          type=verbs.Types.GODAN, ending="ru",
                          english="to go home")

        # often written as kana alone
        self.suru = Verb(kana=u"する", kanji=u"",
                         type=verbs.Types.SURU, ending="irr",
                         english="to do")

        self.fukusuru = Verb(kana=u"ふくする", kanji=u"復する",
                             type=verbs.Types.SURU, ending="irr",
                             english="to return to normal")

        self.kuru = Verb(kana=u"くる", kanji=u"来る",
                         type=verbs.Types.KURU, ending="sp",
                         english="to come")

        self.iku = Verb(kana=u"いく", kanji=u"行く",
                        type=verbs.Types.GODAN, ending="iku",
                        english="to go, to move")


class TestVerbPlainForm(TestVerbClass):

    def test_get_plain(self):
        self.assertEqual(self.au.plain(), u"会う")
        self.assertEqual(self.au.plain(kanji=False), u"あう")

        #test verb with no kanji
        self.assertEqual(self.segamu.plain(), u"せがむ")

    def test_get_ichidan_plain_negative(self):
        self.assertEqual(u"食べない", self.taberu.plain(negative=True))

    def test_get_godan_plain_negative_u_ending(self):
        self.assertEqual(u"会わない", self.au.plain(negative=True))

    def test_get_godan_plain_negative_tsu_ending(self):
        self.assertEqual(u"待たない", self.matsu.plain(negative=True))

    def test_get_godan_plain_negative_su_ending(self):
        self.assertEqual(u"押さない", self.osu.plain(negative=True))

    def test_get_godan_plain_negative_mu_ending(self):
        self.assertEqual(u"飲まない", self.nomu.plain(negative=True))

    def test_get_godan_plain_negative_ku_ending(self):
        self.assertEqual(u"弾かない", self.hiku.plain(negative=True))

    def test_get_godan_plain_negative_gu_ending(self):
        self.assertEqual(u"泳がない", self.oyogu.plain(negative=True))

    def test_get_godan_plain_negative_nu_ending(self):
        self.assertEqual(u"死なない", self.shinu.plain(negative=True))

    def test_get_godan_plain_negative_bu_ending(self):
        self.assertEqual(u"遊ばない", self.asobu.plain(negative=True))

    def test_get_godan_plain_negative_ru_ending(self):
        self.assertEqual(u"帰らない", self.kaeru.plain(negative=True))

    def test_get_aru_plain_negative(self):
        aru = Verb(kana=u"ある",
                   type=verbs.Types.GODAN, ending="irr",
                   english="to be (inanimate objects), to exist")
        self.assertEqual(u"ない", aru.plain(negative=True))

    def test_get_suru_plain_negative(self):
        self.assertEqual(u"しない", self.suru.plain(negative=True))

    def test_get_kuru_plain_negative(self):
        self.assertEqual(u"来ない", self.kuru.plain(negative=True))
        self.assertEqual(u"こない", self.kuru.plain(negative=True, kanji=False))

    def test_get_inflection(self):
        self.assertEqual(self.au.get_inflection(verbs.Inflections.PLAIN),
                         u"会う")
        self.assertEqual(self.au.get_inflection(
                         verbs.Inflections.PLAIN, kanji=False), u"あう")


class TestVerbMasuForm(TestVerbClass):

    def test_get_ichidan_masu(self):
        self.assertEqual(u"食べます", self.taberu.masu())

    def test_get_godan_masu_u_ending(self):
        self.assertEqual(u"会います", self.au.masu())

    def test_get_godan_masu_tsu_ending(self):
        self.assertEqual(u"待ちます", self.matsu.masu())

    def test_get_godan_masu_su_ending(self):
        self.assertEqual(u"押します", self.osu.masu())

    def test_get_godan_masu_mu_ending(self):
        self.assertEqual(u"飲みます", self.nomu.masu())

    def test_get_godan_masu_ku_ending(self):
        self.assertEqual(u"弾きます", self.hiku.masu())

    def test_get_godan_masu_gu_ending(self):
        self.assertEqual(u"泳ぎます", self.oyogu.masu())

    def test_get_godan_masu_nu_ending(self):
        self.assertEqual(u"死にます", self.shinu.masu())

    def test_get_godan_masu_bu_ending(self):
        self.assertEqual(u"遊びます", self.asobu.masu())

    def test_get_godan_masu_ru_ending(self):
        self.assertEqual(u"帰ります", self.kaeru.masu())

    def test_get_suru_masu(self):
        self.assertEqual(u"します", self.suru.masu())
        self.assertEqual(u"復します", self.fukusuru.masu())

    def test_get_kuru_masu(self):
        self.assertEqual(u"来ます", self.kuru.masu())
        self.assertEqual(u"きます", self.kuru.masu(kanji=False))

    def test_masu_negative(self):
        self.assertEqual(u"食べません", self.taberu.masu(negative=True))
        self.assertEqual(u"たべません", self.taberu.masu(negative=True,
                                                              kanji=False))

    def test_masu_past(self):
        self.assertEqual(u"食べました", self.taberu.masu(tense=Verb.PAST))
        self.assertEqual(u"たべました", self.taberu.masu(tense=Verb.PAST,
                                                              kanji=False))

    def test_masu_negative_past(self):
        self.assertEqual(u"食べませんでした",
                         self.taberu.masu(
                             negative=True,
                             tense=Verb.PAST))


class TestVerbTeForm(TestVerbClass):

    def test_get_ichidan_te_form(self):
        self.assertEqual(u"食べて", self.taberu.te())

    def test_get_godan_te_form_u_ending(self):
        self.assertEqual(u"会って", self.au.te())
        self.assertEqual(u"あって", self.au.te(kanji=False))

    def test_get_godan_te_form_tsu_ending(self):
        self.assertEqual(u"待って", self.matsu.te())

    def test_get_godan_te_form_ru_ending(self):
        self.assertEqual(u"帰って", self.kaeru.te())

    def test_get_godan_te_form_mu_ending(self):
        self.assertEqual(u"飲んで", self.nomu.te())

    def test_get_godan_te_form_bu_ending(self):
        self.assertEqual(u"遊んで", self.asobu.te())

    def test_get_godan_te_form_nu_ending(self):
        self.assertEqual(u"死んで", self.shinu.te())

    def test_get_godan_te_form_ku_ending(self):
        self.assertEqual(u"弾いて", self.hiku.te())

    def test_get_godan_te_form_gu_ending(self):
        self.assertEqual(u"泳いで", self.oyogu.te())

    def test_get_godan_te_form_su_ending(self):
        self.assertEqual(u"押して", self.osu.te())

    def test_get_iku_te_form(self):
        self.assertEqual(u"行って", self.iku.te())


if __name__ == "__main__":
    unittest.main()
