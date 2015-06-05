# Possibly used for doing all database stuff but at the very least setting up
# the database

import urllib
import os
import gzip
import sqlite3
import re
import verbs

import xml.etree.ElementTree as ET


JMDICT_URL = "http://ftp.monash.edu.au/pub/nihongo/JMdict_e.gz"


def init(path, jlpt_dictionary):
    print("downloading JMDict dictionary...")
    directory = os.path.dirname(path)
    dictionary_file = os.path.join(directory, "JMDict_e.gz")
    if not os.path.isfile(dictionary_file):
        urllib.urlretrieve(JMDICT_URL, dictionary_file)

    print("unpacking dictionary...")
    f = gzip.open(dictionary_file, 'rb')
    raw_xml = f.read()
    f.close()

    print("parsing data...")
    dictionary = ET.fromstring(raw_xml)

    print("creating emtpy database...")
    db = sqlite3.connect(path)
    cur = db.cursor()

    # maybe drop table before hand if table exits already
    print("creating tables...")
    cur.execute('''DROP TABLE IF EXISTS verbs''')
    cur.execute('''CREATE TABLE verbs (
                    id INTEGER PRIMARY KEY,
                    kana TEXT,
                    kanji TEXT,
                    type TEXT,
                    ending TEXT,
                    english TEXT,
                    jlpt INTEGER)''')

    print("populating tables...")
    verb_entries = [entry for entry in dictionary
                    if " verb" in entry.find('sense').find('pos').text]

    for verb in verb_entries:
        seq = verb.find('ent_seq').text
        kana = verb.find('r_ele')[0].text

        kanji_container = verb.find('k_ele')
        kanji = ""
        if kanji_container is not None:
            kanji = kanji_container[0].text

        sense = verb.find('sense')

        verb_type, ending = get_verb_type(sense.find('pos').text)

        if not verb_type or not ending:
            continue

        english = ", ".join([gloss.text
                             for gloss in sense.findall('gloss')])

        jlpt = jlpt_dictionary.get((kanji, kana), 0)

        cur.execute('INSERT INTO verbs VALUES (?,?,?,?,?,?,?)',
                    [seq, kana, kanji, verb_type, ending, english, jlpt])

    db.commit()
    cur.execute('SELECT * FROM verbs')
    print("{0} verbs added".format(len(cur.fetchall())))


def get_verb_type(description):
    verb_type = None
    ending = None
    if description.startswith("Godan"):
        verb_type = verbs.Types.GODAN
    elif description.startswith("Ichidan"):
        verb_type = verbs.Types.ICHIDAN
    elif description.startswith("Kuru"):
        verb_type = verbs.Types.KURU
    elif description.startswith("suru"):
        verb_type = verbs.Types.SURU

    match = re.search('`([bgkmrts]*?u)\'', description)
    if match:
        ending = match.group(1)
    elif "Iku" in description:
        ending = "iku"
    elif "-aru" in description:
        ending = "aru"
    elif description is "kuru":
        ending = "kuru"
    elif "zuru" in description:
        ending = "zuru"
    elif "kureru" in description:
        ending = "kureru"
    elif verb_type is "ichidan":
        ending = "ru"
    elif "special" in description:
        ending = "sp"
    elif "irregular" in description:
        ending = "irr"

    return verb_type, ending


def is_initialized(db_path):

    if os.path.isfile(db_path):
        db = Database(db_path)
        return db.is_initialized()

    return False


class Database(object):
    ''' Class used for handling database connections '''

    def __init__(self, db_path):
        if not os.path.isfile(db_path):
            print("Creating new sqlite database at {}".format(db_path))

        self.db = sqlite3.connect(db_path)
        self.db.row_factory = sqlite3.Row
        self.cur = self.db.cursor()

    def is_initialized(self):
        entry_count = self.cur.execute(''' SELECT COUNT(*) FROM verbs ''')
        return entry_count > 0

    def get_verb(self, **kwargs):
        verb_type = kwargs.get('type', None)
        where_statement = ""

        if verb_type:
            where_statement += "WHERE type='{0}' ".format(verb_type)

        command = ("SELECT * FROM verbs {0}"
                   "ORDER BY RANDOM() LIMIT 1".format(where_statement))

        self.cur.execute(command)
        return self.cur.fetchone()
