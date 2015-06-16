# -*- coding: utf-8 -*-
import textwrap
import views.interface
from lib.verbs import Inflections
from controllers.verbquiz import StandardConfig  # Might be circular...


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
        print(self.format_option_table(StandardConfig.All_readable_dict()))

    def ask_for_custom_config(self):
        print(u"から:")
        print(self.format_option_table(
              Inflections.All_readable_dict()))

    def format_option_table(self, options):
        spaced_inflections = ""
        for k, v in options.items():
            inflection = "{0}: {1}".format(k, v)
            spaced_inflections += inflection.ljust(26)
        return textwrap.fill(spaced_inflections, 78)
