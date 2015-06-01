# Possibly used for doing all database stuff but at the very least setting up
# the database

import urllib
import os
import sys
import gzip
import sqlite3

import xml.etree.ElementTree as ET


JMDICT_URL = "http://ftp.monash.edu.au/pub/nihongo/JMdict_e.gz"


def init_database(path):
    print("downloading JMDict dictionary...")
    destination = os.path.join(path, "JMDict_e.gz")
    urllib.urlretrieve(JMDICT_URL, destination)

    print("unpacking dictionary...")
    f = gzip.open(destination, 'rb')
    raw_xml = f.read()
    f.close()

    print("parsing data...")
    dictionary = ET.fromstring(raw_xml)

    print("creating emtpy database...")
    conn = sqlite3.connect(os.path.join(path, "verbs.db"))
    cur = conn.cursor()

    # maybe drop table before hand if table exits already
    print("creating tables...")
    cur.execute('''CREATE TABLE verbs (
                    id INTEGER PRIMARY KEY,
                    kana TEXT,
                    kanji TEXT,
                    type TEXT,
                    english TEXT
                    jlpt INTEGER)''')

    print("populating tables...")
    verbs = [entry for entry in dictionary
             if " verb" in entry.find('sense').find('pos').text]

    for idx, verb in enumerate(verbs):
        kana = verb.find('r_ele')[0].text

        kanji_container = verb.find('k_ele')[0]
        kanji = ""
        if kanji_container is not None:
            kanji = kanji_container.text

        sense = verb.find('sense')

        verb_type = sense.find('pos').text
        english = ", ".join([gloss.text
                            for gloss in sense.findall('gloss')])
        jlpt = 0  # for now

        cur.execute('INSERT INTO verbs VALUES (?,?,?,?,?)',
                    [kana, kanji, verb_type, english, jlpt])

        if idx % 10 is 0:
            sys.stdout.write('.')

    print("{0} verbs added".format(idx))
