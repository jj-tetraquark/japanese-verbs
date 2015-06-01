# Possibly used for doing all database stuff but at the very least setting up
# the database

import urllib
import os
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

    print("creating tables...")
    cur.execute('''CREATE TABLE verbs (
                    id INTEGER PRIMARY KEY,
                    kana text,
                    kanji text,
                    type text,
                    english text)''')

    print("populating tables...")
    verbs = [entry for entry in dictionary
             if "verb" in entry.find('sense').find('pos').text]
    print("{0} verbs found".format(len(verbs)))
