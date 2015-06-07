#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import lib.database as database
import lib.verbs as verbs
from lib.verbs import Verb

DB_PATH = 'data/data.db'


@unittest.skipIf(
    not database.is_initialized(DB_PATH),
    "Database not initialized, need install before running this suite")
class TestDatabaseConnections(unittest.TestCase):

    def setUp(self):
        self.db = database.Database(DB_PATH)

    def test_get_random_verb(self):
        verb = self.db.get_verb()
        self.assertNotEqual(verb["kana"], "")  # kana should never be empty

    def test_get_all_verb_types(self):
        for v_type in verbs.Types.All():
            verb = self.db.get_verb(type=v_type)
            self.assertEqual(verb["type"], v_type)


class TestVerbObject(unittest.TestCase):
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

    def test_get_plain(self):
        self.assertEqual(self.au.plain(), u"会う")
        self.assertEqual(self.au.plain(kanji=False), u"あう")

        #test verb with no kanji
        self.assertEqual(self.segamu.plain(), u"せがむ")

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


if __name__ == "__main__":
    unittest.main()
