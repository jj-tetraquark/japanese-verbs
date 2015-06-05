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
        au = verbs.Verb(kana="あう",
                        kanji="会う",
                        type=verbs.Types.GODAN,
                        ending="u",
                        english="to meet")
        self.assertEqual(au.plain(), "会う")

        segamu = verbs.Verb(kana="せがむ",
                            kanji="",
                            type=verbs.Types.GODAN,
                            ending="mu",
                            english="to pester")
        self.assertEqual(segamu.plain(), "せがむ")


if __name__ == "__main__":
    unittest.main()
