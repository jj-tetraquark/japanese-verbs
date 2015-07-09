#!/usr/bin/env python
import os
import threading
import lib.database as database
from controllers.verbquiz import VerbQuizController
from views.cli import CLIView
from views.web import WebView


def main():
    if is_first_run():
        do_installation()
    #view = CLIView()
    view = WebView()
    controller = VerbQuizController(view)

    view.init_splash()

    control_thread = threading.Thread(target=controller.start)
    control_thread.start()
    controller.wait_for_quiz_to_finish()
    control_thread.join()


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
