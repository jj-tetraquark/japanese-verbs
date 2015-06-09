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


class Verb(object):
    ''' Wrapper to handle most verb stuff '''

    PAST = 1
    PRESENT = 0

    def __init__(self, **kwargs):
        self.kana = kwargs.get("kana")
        self.kanji = kwargs.get("kanji")
        self.type = kwargs.get("type")
        self.ending = kwargs.get("ending")
        self.english = kwargs.get("english")

        if not self.kana:
            raise ValueError("kana cannot be empty")
        if not self.type in Types.All():
            raise ValueError("Invalid type passed: {0}".format(self.type))
        if not self.ending:
            raise ValueError("ending cannot be empty")

    @classmethod
    def from_dict(cls, dic):
        return cls(kana=dic["kana"],
                   kanji=dic["kanji"],
                   type=dic["type"],
                   ending=dic["ending"],
                   english=dic["english"])

    def plain(self, **kwargs):
        use_kanji = kwargs.get("kanji", True)
        negative = kwargs.get("negative", False)
        stem = self.kanji if use_kanji and self.kanji else self.kana

        if not negative:
            return stem
        else:
            return self.__get_plain_negative_stem(stem) + u"ない"

    def masu(self, **kwargs):
        plain_form = self.plain(kanji=kwargs.get("kanji", True))
        negative = kwargs.get("negative", False)
        tense = kwargs.get("tense", Verb.PRESENT)

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
            if self.ending in ["u", "tsu", "ru"]:
                return plain_form[:-1] + u"って"
            elif self.ending in ["bu", "nu", "mu"]:
                return plain_form[:-1] + u"んで"
            elif self.ending == "ku":
                return plain_form[:-1] + u"いて"
            elif self.ending == "gu":
                return plain_form[:-1] + u"いで"
            elif self.ending == "su":
                return plain_form[:-1] + u"して"

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
                              "ru": u"ら"}
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
                          "ru": u"り"}
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
