# Possibly used for doing all database stuff but at the very least setting up
# the database

import urllib
import os
import sys
import gzip
import sqlite3
import re

import xml.etree.ElementTree as ET


JMDICT_URL = "http://ftp.monash.edu.au/pub/nihongo/JMdict_e.gz"


def init_database(path):
    print("downloading JMDict dictionary...")
    destination = os.path.join(path, "JMDict_e.gz")
    if not os.path.isfile(destination):
        urllib.urlretrieve(JMDICT_URL, destination)

    print("unpacking dictionary...")
    f = gzip.open(destination, 'rb')
    raw_xml = f.read()
    f.close()

    print("parsing data...")
    dictionary = ET.fromstring(raw_xml)

    print("creating emtpy database...")
    db = sqlite3.connect(os.path.join(path, "verbs.db"))
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
    verbs = [entry for entry in dictionary
             if " verb" in entry.find('sense').find('pos').text]

    for verb in verbs:
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
        jlpt = 0  # for now

        cur.execute('INSERT INTO verbs VALUES (?,?,?,?,?,?,?)',
                    [seq, kana, kanji, verb_type, ending, english, jlpt])

    db.commit()
    cur.execute('SELECT * FROM verbs')
    print("{0} verbs added".format(len(cur.fetchall())))


def get_verb_type(description):
    verb_type = None
    ending = None
    if description.startswith("Godan"):
        verb_type = "godan"
    elif description.startswith("Ichidan"):
        verb_type = "ichidan"
    elif description.startswith("Kuru"):
        verb_type = "kuru"
    elif description.startswith("suru"):
        verb_type = "suru"


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
