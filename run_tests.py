#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import lib.database as database
import lib.verbs as verbs

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

    def test_get_plain(self):
        au = verbs.Verb(kana=u"あう",
                        kanji=u"会う",
                        type=verbs.Types.GODAN,
                        ending="u",
                        english="to meet")
        self.assertEqual(au.plain(), u"会う")
        self.assertEqual(au.plain(kanji=False), u"あう")

        segamu = verbs.Verb(kana=u"せがむ",
                            type=verbs.Types.GODAN,
                            ending="mu")
        self.assertEqual(segamu.plain(), u"せがむ")

    def test_get_ichidan_masu(self):
        taberu = verbs.Verb(kana=u"たべる",
                            kanji=u"食べる",
                            type=verbs.Types.ICHIDAN,
                            ending="ru")
        self.assertEqual(u"食べます", taberu.masu())

    def test_get_godan_masu_u_ending(self):
        au = verbs.Verb(kana=u"あう",
                        kanji=u"会う",
                        type=verbs.Types.GODAN,
                        ending="u",
                        english="to meet")
        self.assertEqual(u"会います", au.masu())

    def test_get_godan_masu_tsu_ending(self):
        matsu = verbs.Verb(kana=u"まつ",
                           kanji=u"待つ",
                           type=verbs.Types.GODAN,
                           ending="tsu",
                           english="to wait")
        self.assertEqual(u"待ちます", matsu.masu())

    def test_get_godan_masu_su_ending(self):
        osu = verbs.Verb(kana=u"おす",
                         kanji=u"押す",
                         type=verbs.Types.GODAN,
                         ending="su",
                         english="to push, to press")
        self.assertEqual(u"押します", osu.masu())

    def test_get_godan_masu_mu_ending(self):
        nomu = verbs.Verb(kana=u"のむ",
                          kanji=u"飲む",
                          type=verbs.Types.GODAN,
                          ending="mu",
                          english="to drink, to swallow")
        self.assertEqual(u"飲みます", nomu.masu())

    def test_get_godan_masu_ku_ending(self):
        hiku = verbs.Verb(kana=u"ひく",
                          kanji=u"弾く",
                          type=verbs.Types.GODAN,
                          ending="ku",
                          english="to play(piano or guitar)")
        self.assertEqual(u"弾きます", hiku.masu())

    def test_get_godan_masu_gu_ending(self):
        oyogu = verbs.Verb(kana=u"およぐ",
                           kanji=u"泳ぐ",
                           type=verbs.Types.GODAN,
                           ending="gu",
                           english="to swim")
        self.assertEqual(u"泳ぎます", oyogu.masu())

    def test_get_godan_masu_nu_ending(self):
        shinu = verbs.Verb(kana=u"しぬ",
                           kanji=u"死ぬ",
                           type=verbs.Types.GODAN,
                           ending="nu",
                           english="to die")
        self.assertEqual(u"死にます", shinu.masu())

    def test_get_godan_masu_bu_ending(self):
        asobu = verbs.Verb(kana=u"あそぶ",
                           kanji=u"遊ぶ",
                           type=verbs.Types.GODAN,
                           ending="bu",
                           english="to play")
        self.assertEqual(u"遊びます", asobu.masu())

    def test_get_godan_masu_ru_ending(self):
        kaeru = verbs.Verb(kana=u"かえる",
                           kanji=u"帰る",
                           type=verbs.Types.GODAN,
                           ending="ru",
                           english="to go home")
        self.assertEqual(u"帰ります", kaeru.masu())

    def test_get_suru_masu(self):
        suru = verbs.Verb(kana=u"する",
                          kanji=u"",  # often written as kana alone
                          type=verbs.Types.SURU,
                          ending="irr",
                          english="to do")
        self.assertEqual(u"します", suru.masu())

        fukusuru = verbs.Verb(kana=u"ふくする",
                              kanji=u"復する",
                              type=verbs.Types.SURU,
                              ending="irr",
                              english="to return to normal")
        self.assertEqual(u"復します", fukusuru.masu())

    def test_get_kuru_masu(self):
        kuru = verbs.Verb(kana=u"くる",
                          kanji=u"来る",
                          type=verbs.Types.KURU,
                          ending="sp",
                          english="to come")
        self.assertEqual(u"来ます", kuru.masu())
        self.assertEqual(u"きます", kuru.masu(kanji=False))


if __name__ == "__main__":
    unittest.main()
