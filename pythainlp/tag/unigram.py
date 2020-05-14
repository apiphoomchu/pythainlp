# -*- coding: utf-8 -*-
"""
Unigram Part-Of-Speech Tagger
"""
import json
import os
from typing import List, Tuple

import dill
import nltk.tag
from pythainlp.corpus import corpus_path
from .orchid_preprocessing import orchid_preprocessing, orchid_tag_to_text

_THAI_POS_ORCHID_FILENAME = "orchid_pos_th.json"
_THAI_POS_ORCHID_PATH = os.path.join(corpus_path(), _THAI_POS_ORCHID_FILENAME)
_THAI_POS_PUD_FILENAME = "ud_thai_pud_unigram_tagger.json"
_THAI_POS_PUD_PATH = os.path.join(corpus_path(), _THAI_POS_PUD_FILENAME)

def _find_tag(words:list, dictdata:dict):
    _temp = []
    _word = list(dictdata.keys())
    for word in words:
        if word in _word:
            _temp.append((word, dictdata[word]))
        else:
            _temp.append((word, None))
    return _temp

def _orchid_tagger():
    with open(_THAI_POS_ORCHID_PATH, encoding="utf-8-sig") as f:
        model = json.load(f)
    return model


def _pud_tagger():
    with open(_THAI_POS_PUD_PATH, encoding="utf-8-sig") as f:
        model = json.load(f)
    return model


def tag(words: List[str], corpus: str) -> List[Tuple[str, str]]:
    """
    รับค่าเป็น ''list'' คืนค่าเป็น ''list'' เช่น [('คำ', 'ชนิดคำ'), ('คำ', 'ชนิดคำ'), ...]
    """
    if not words:
        return []

    if corpus == "orchid":
        i = 0
        words = orchid_preprocessing(words)
        t = _find_tag(words, _orchid_tagger())
        temp = []
        i = 0
        while i < len(t):
            word = orchid_tag_to_text(t[i][0])
            tag = t[i][1]
            temp.append((word, tag))
            i += 1
        t = temp
    else:
        t = _find_tag(words, _pud_tagger())

    return t
