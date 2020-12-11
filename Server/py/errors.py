# -*- coding: utf-8 -*-

class ArgumentError(Exception):
    def __init__(self, text):
        self.text = text
