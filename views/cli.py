# -*- coding: utf-8 -*-
import textwrap
import os
import time
import sys
import locale
import views.interface
import lib.verbs as verbs
from controllers.verbquiz import StandardConfig  # Might be circular...

# Python 2 shim
try:
    input = raw_input
except NameError:
    pass


def u_input(text):
    try:
        return raw_input(text).decode(
            sys.stdin.encoding or locale.getpreferredencoding(True))
    except NameError:
        return input(text)


class CLIView(views.interface.QuizView):
    ''' Basic Command Line View '''

    def __init__(self):
        super(CLIView, self).__init__()
        self.inflections = verbs.Inflections.All_readable_dict()

    def init_splash(self):
        self.clear_terminal()
        #日本語の動詞
        print('''
                 ├───────┐  ____│____  ___\__ ¯¯/¯¯¯¯      #####
                 │       │     /│\      ────  -/---┐     #   #  #
                 ├───────┤    / │ \     ──── _/____|_   #   #    #
                 │       │   /  │  \    ┌──┐  ┌────┐     # #    #
                 ├───────┤  ¯  ─┼─  ¯   ├──┤  ├────┤      *    *

                      --──┬─¯¯¯   │           \ 
                      ────┼──── ──┼───┐   ──────── ───────┐
                      ┌───┼───┐   │   │    ──────  ────── │
                      ├───┼───┤   │   │    ──────  ┌────┐ │
                      └───┼───┘   │   │    ├────┐  │    │ │
                      ────┼────   /   │    │    │  ├────┘ │
                      _--─┴─¯¯¯  / --─┘    ├────┤       -_/

                               にほんのどうし
        ''')

    def ask_user_for_config(self):
        print(u"動詞質問はどれですか\n====================")

        inflection_config = self.ask_for_selection_from_dictonary(
            StandardConfig.All_readable_dict())

        if inflection_config is StandardConfig.CUSTOM:
            sys.exit("Not supported yet!")

        print("")
        number_of_questions = self.ask_for_number("何問ですか: ")

        print(u"JLPTのだんかいは何ですか")
        jlpt = self.ask_for_selection_from_dictonary(
            verbs.JLPTLevel.All_readable_dict())

        self.set_quiz_config(
            {"number_of_questions": number_of_questions,
             "inflections": StandardConfig.get_config(inflection_config),
             "jlpt": jlpt})

    def ask_for_custom_config(self):
        print(u"から:")
        print(self.format_option_table(
            verbs.Inflections.All_readable_dict()))

    def display_start_quiz(self):
        print(u"\n=================\nよし！がんばって！\n=================\n")
        time.sleep(1)
        self.clear_terminal()

    def do_ask_question(self, asks, predicate):
        print(u" しつもん ".center(40, "="))
        self.print_kanji_kana(predicate)
        answer = u_input(u"{0} : ".format(self.inflections[asks]))
        self.submit_answer(answer)

    def do_handle_answer_result(self, is_correct, correct_answer):
        print(u"-" * 40)
        print("")
        if is_correct:
            print(u"\u25CB  せいかいです!")
        else:
            print(u"\u2716  まちがいです。")
            self.print_kanji_kana(correct_answer)
        print("")
        print(u"-" * 40)
        time.sleep(1)
        self.request_next_question()

    def on_finish_quiz(self, data):
        self.clear_terminal()
        print(u"=" * 80)
        print(u"おめでとう！クイズがかんせいです".center(80))
        print(u"=" * 80)
        print(u"\u25CB  せいかい : {0}".format(data["correct_answers"]))
        print(u"\u2716  まちがい : {0}".format(data["quiz_length"] -
                                           data["correct_answers"]))

    def print_kanji_kana(self, kanji_kana_tuple):
        print(u"\n{0} [{1}]".format(kanji_kana_tuple[0], kanji_kana_tuple[1]))

    def ask_for_number(self, question):
        while True:
            number = input(question)
            if number.isdigit():
                return int(number)
            else:
                print(u"分かりません。もう一度数をください")

    def ask_for_selection_from_dictonary(self, options):
        print(self.format_option_table(options))
        while True:
            selection = input(
                "選んでください [1 - {}]: ".format(len(options) - 1))

            if selection.isdigit():
                selection = int(selection)
            if options.get(selection, None):
                return selection
            else:
                print(u"分かりません。もう一度")

    def format_option_table(self, options):
        spaced_inflections = ""
        for k, v in options.items():
            inflection = "{0}: {1}".format(k, v)
            spaced_inflections += inflection.ljust(26)
        return textwrap.fill(spaced_inflections, 78)


    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')
