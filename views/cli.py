# -*- coding: utf-8 -*-
import textwrap
import views.interface
from lib.verbs import Inflections

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
        print(u"から:")
        print self.formatted_inflection_table()

    def formatted_inflection_table(self):
        spaced_inflections = ""
        for k, v in Inflections.All_readable_dict().items():
            inflection = "{0}: {1}".format(k, v)
            spaced_inflections += inflection.ljust(26)
        return textwrap.fill(spaced_inflections, 78)



