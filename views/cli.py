# -*- coding: utf-8 -*-
import textwrap
import sys
import views.interface
import lib.verbs as verbs
from controllers.verbquiz import StandardConfig  # Might be circular...

# Python 2 shim
try:
    input = raw_input
except NameError:
    pass

class CLIView(views.interface.QuizView):
    ''' Basic Command Line View '''

    def __init__(self):
        super(CLIView, self).__init__()

    def init_splash(self):
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
        print(u"動詞質問はどれですか\n####################")

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
                "選んでください [1 - {}]: ".format(len(options) -1))

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
