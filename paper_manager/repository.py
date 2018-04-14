# coding=utf-8
# @author=cer


class Repository:
    def __init__(self, name, path, support_suffix=None):
        """
        :param name: name of the repository
        :param path: absolute path of the repository
        :param support_suffix: support suffix of this repository
        """
        self.name = name
        self.path = path
        if support_suffix is None:
            self.support_suffix = ["pdf"]
        else:
            self.support_suffix = support_suffix

