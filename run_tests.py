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



if __name__ == "__main__":
    unittest.main()
