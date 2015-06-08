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
        return self.kanji if use_kanji and self.kanji else self.kana

    def masu(self, **kwargs):
        stem = self.plain(kanji=kwargs.get("kanji", True))
        negative = kwargs.get("negative", False)
        tense = kwargs.get("tense", Verb.PRESENT)

        conjugated = self.__get_masu_stem(stem)
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

