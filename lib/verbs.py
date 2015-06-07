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

    def plain(self):
        return self.kanji if self.kanji else self.kana

    #TODO: should take kwargs with kanji=True/False
    def masu(self, **kwargs):

        stem = self.kanji if kwargs.get("kanji", True) else self.kana

        if self.type is Types.ICHIDAN:
            return stem[:-1] + u"ます"
        elif self.type is Types.GODAN:
            if self.ending is "u":
                return stem[:-1] + u"います"
            elif self.ending is "tsu":
                return stem[:-1] + u"ちます"
            elif self.ending is "su":
                return stem[:-1] + u"します"
            elif self.ending is "mu":
                return stem[:-1] + u"みます"
            elif self.ending is "ku":
                return stem[:-1] + u"きます"
            elif self.ending is "gu":
                return stem[:-1] + u"ぎます"
            elif self.ending is "nu":
                return stem[:-1] + u"にます"
            elif self.ending is "bu":
                return stem[:-1] + u"びます"
            elif self.ending is "ru":
                return stem[:-1] + u"ります"
        elif self.type is Types.SURU:
            return stem[:-2] + u"します"
        elif self.type is Types.KURU:
            if u"来" in stem:
                return stem[:-1] + u"ます"
            else:
                return stem[:-2] + u"きます"
        else:
            raise TypeError("Unrecognised verb type!")

