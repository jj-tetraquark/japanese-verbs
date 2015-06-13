import lib.database as db
import lib.verbs as verbs


class VerbTestController(object):

    def __init__(self):
        # probably should make db configurable
        self.db = db.Database(db.DEFAULT_DATABASE_PATH)
