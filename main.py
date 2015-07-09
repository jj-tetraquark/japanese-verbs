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

    # This needs to be sorted out. It's currently broken for WebView because start()
    # starts the server and is blocking. The controller never gets started. The controller
    # should be started first in its own thread and it should wait until the view has started
    # before asking the user for config.
    # The view needs to be started in the main thread

    controller.start()
    view.start()
    controller.wait_for_quiz_to_finish()


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
