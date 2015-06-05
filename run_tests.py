#!/usr/bin/env python

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
        verb_types = [verbs.ICHIDAN, verbs.GODAN, verbs.KURU, verbs.SURU]
        for v_type in verb_types:
            verb = self.db.get_verb(type=v_type)
            self.assertEqual(verb["type"], v_type)


if __name__ == "__main__":
    unittest.main()
