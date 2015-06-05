#!/usr/bin/env python

import unittest
import lib.database as database

DB_PATH = 'data/data.db'

@unittest.skipIf(not database.is_initialized(DB_PATH),
        "Database not initialized, need install before running this suite")
class TestDatabaseConnections(unittest.TestCase):

    def test_get_random_verb(self):
        db = database.Database(DB_PATH)
        verb = db.get_verb()
        self.assertNotEqual(verb["kana"], "") # kana should never be empty




if __name__ == "__main__":
    unittest.main()
