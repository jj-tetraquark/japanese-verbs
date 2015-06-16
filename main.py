#!/usr/bin/env python

import os
import lib.database as database
from controllers.verbquiz import VerbQuizController
from views.cli import CLIView


def main():
    if is_first_run():
        do_installation()
    view = CLIView()
    controller = VerbQuizController(view)

    view.init_splash()
    controller.start()


def is_first_run():
    return not os.path.isfile('data/data.db')


def do_installation():
    print("Running first time installation...")
    database.init('data/data.db', build_jlpt_dict())


def build_jlpt_dict():
    print("Building jlpt dictionary..")
    jlpt = dict()
    for x in range(1, 6):
        print("jlpt{0}".format(x))
        datfile = "data/jlpt{0}.dat".format(x)

        with open(datfile) as f:
            for line in f.readlines():
                kanji, kana = line.split(',')
                if '-' in kanji:
                    kanji = ""

                kana = kana.rstrip()

                jlpt[(kanji.decode('utf-8'), kana.decode('utf-8'))] = x

    return jlpt


if __name__ == "__main__":
    main()
