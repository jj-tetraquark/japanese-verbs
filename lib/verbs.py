# -*- coding: utf-8 -*-
# Verb types as string constants

class Types(object):
    ICHIDAN = "ichidan"
    GODAN = "godan"
    KURU = "kuru"
    SURU = "suru"

    @classmethod
    def All(cls):
        return [cls.ICHIDAN, cls.GODAN, cls.KURU, cls.SURU]


class Inflections(object):
    PLAIN = 1
    NEGATIVE_PLAIN = 2
    PAST_PLAIN = 3
    NEGATIVE_PAST_PLAIN = 4
    POLITE = 5
    NEGATIVE_POLITE = 6
    PAST_POLITE = 7
    NEGATIVE_PAST_POLITE = 8
    TE_FORM = 9
    PASSIVE = 10
    CAUSATIVE = 11
    PASSIVE_CAUSATIVE = 12

    @classmethod
    def AllAttr(cls):
        return [i for i in dir(cls) if not callable(i)
                and not (i.startswith("__") or i.startswith("All"))]

    @classmethod
    def All_readable_dict(cls):
        return {getattr(cls, i): i.replace('_', ' ').title()
                for i in cls.AllAttr()}

class JLPTLevel:
    N1 = 1
    N2 = 2
    N3 = 3
    N4 = 4
    N5 = 5
    NON_JLPT = 0

    @classmethod
    def AllJLPT(cls):
        return [cls.N1, cls.N2, cls.N3, cls.N4, cls.N5]

    @classmethod
    def All(cls):
        return cls.AllJLPT() + [cls.NON_JLPT]

    @classmethod
    def All_attr(cls):
        return [i for i in dir(cls) if not callable(getattr(cls, i))
                and not i.startswith("__")]

    @classmethod
    def All_readable_dict(cls):
        return {getattr(cls, i): i.replace('_', ' ').title()
                for i in cls.All_attr()}

class Verb(object):
    ''' Wrapper to handle most verb stuff '''

    PAST = 1
    NON_PAST = 0

    def __init__(self, **kwargs):
        self.kana = kwargs.get("kana")
        self.kanji = kwargs.get("kanji")
        self.type = kwargs.get("type")
        self.ending = kwargs.get("ending")
        self.english = kwargs.get("english")
        self.jlpt = kwargs.get("jlpt")

        if not self.kana:
            raise TypeError("kana cannot be empty")
        if not self.type in Types.All():
            raise TypeError("Invalid type passed: {0}".format(self.type))
        if not self.ending:
            raise TypeError("ending cannot be empty")

    def get_inflection(self, infl, kanji=True, kana=False):
        I = Inflections

        not_implemented = lambda k: NotImplementedError("Not yet")
        inflection_method_lookup = {
            I.PLAIN:
            lambda k: self.plain(kanji=k),
            I.NEGATIVE_PLAIN:
            lambda k: self.plain(negative=True, kanji=k),
            I.PAST_PLAIN:
            lambda k: self.plain(tense=Verb.PAST, kanji=k),
            I.NEGATIVE_PAST_PLAIN:
            lambda k: self.plain(negative=True, tense=Verb.PAST, kanji=k),
            I.POLITE:
            lambda k: self.masu(kanji=k),
            I.NEGATIVE_POLITE:
            lambda k: self.masu(negative=True, kanji=k),
            I.PAST_POLITE:
            lambda k: self.masu(tense=Verb.PAST, kanji=k),
            I.NEGATIVE_PAST_POLITE:
            lambda k: self.masu(tense=Verb.PAST, negative=True, kanji=k),
            I.TE_FORM:
            lambda k: self.te(kanji=k),
            I.PASSIVE:
            not_implemented,
            I.CAUSATIVE:
            not_implemented,
            I.PASSIVE_CAUSATIVE:
            not_implemented
        }
        if not kana:
            return inflection_method_lookup[infl](kanji)
        elif kanji:
            return (inflection_method_lookup[infl](True),
                    inflection_method_lookup[infl](False))

    def plain(self, **kwargs):
        use_kanji = kwargs.get("kanji", True)
        negative = kwargs.get("negative", False)
        tense = kwargs.get("tense", Verb.NON_PAST)

        stem = self.kanji if use_kanji and self.kanji else self.kana

        if not negative:
            if tense is Verb.PAST:
                te_form = self.te(**kwargs)
                if te_form[-1] == u"て":
                    return te_form[:-1] + u"た"
                else:
                    return te_form[:-1] + u"だ"
            else:
                return stem
        else:
            negative_stem = self.__get_plain_negative_stem(stem)
            if tense is Verb.PAST:
                return negative_stem + u"なかった"
            else:
                return negative_stem + u"ない"

    def masu(self, **kwargs):
        plain_form = self.plain(kanji=kwargs.get("kanji", True))
        negative = kwargs.get("negative", False)
        tense = kwargs.get("tense", Verb.NON_PAST)

        conjugated = self.__get_masu_stem(plain_form)
        if negative:
            conjugated += u"せん"
            if tense is Verb.PAST:
                conjugated += u"でした"
        else:
            if tense is Verb.PAST:
                conjugated += u"した"
            else:
                conjugated += u"す"

        return conjugated

    def te(self, **kwargs):
        plain_form = self.plain(kanji=kwargs.get("kanji", True))
        if self.type == Types.ICHIDAN:
            return plain_form[:-1] + u"て"
        else:
            if self.ending in ["u", "tsu", "ru", "iku", "aru"]:
                return plain_form[:-1] + u"って"
            elif self.ending in ["bu", "nu", "mu"]:
                return plain_form[:-1] + u"んで"
            elif self.ending == "ku":
                return plain_form[:-1] + u"いて"
            elif self.ending == "gu":
                return plain_form[:-1] + u"いで"
            elif self.ending == "su":
                return plain_form[:-1] + u"して"
        #TODO suru and kuru

    def __get_plain_negative_stem(self, stem):
        neg_stem = stem[:-1]
        if self.type == Types.GODAN:
            if self.kana == u"ある":
                neg_stem = ""
            else:
                u_to_a_map = {"u": u"わ",
                              "tsu": u"た",
                              "su": u"さ",
                              "mu": u"ま",
                              "ku": u"か",
                              "gu": u"が",
                              "nu": u"な",
                              "bu": u"ば",
                              "ru": u"ら",
                              "iku": u"か",
                              "aru": u"ら"}
                neg_stem += u_to_a_map[self.ending]
        elif self.type == Types.SURU:
            neg_stem = u"し"
        elif self.type == Types.KURU:
            if not u"来" in neg_stem:
                neg_stem = u"こ"

        return neg_stem

    def __get_masu_stem(self, stem):
        masu_stem = None
        if self.type == Types.ICHIDAN:
            masu_stem = stem[:-1] + u"ま"
        elif self.type == Types.GODAN:
            u_to_i_map = {"u": u"い",
                          "tsu": u"ち",
                          "su": u"し",
                          "mu": u"み",
                          "ku": u"き",
                          "gu": u"ぎ",
                          "nu": u"に",
                          "bu": u"び",
                          "ru": u"り",
                          "iku": u"き",
                          "aru": u"い"}
            masu_stem = stem[:-1] + u_to_i_map[self.ending] + u"ま"
        elif self.type == Types.SURU:
            masu_stem = stem[:-2] + u"しま"
        elif self.type == Types.KURU:
            if u"来" in stem:
                masu_stem = stem[:-1] + u"ま"
            else:
                masu_stem = stem[:-2] + u"きま"
        else:
            raise TypeError("Unrecognised verb type!")

        return masu_stem
