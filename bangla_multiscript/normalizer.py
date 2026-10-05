# -*- coding: utf-8 -*-
"""
BanglaMultiScript Text Normalizer Module
Cleans Zero-Width characters (ZWNJ/ZWJ), repeated punctuation, social media letter elongation,
and standardizes Bengali and Banglish text.
"""

import re

# Zero-Width Non-Joiner and Joiner
ZWNJ = '\u200c'
ZWJ = '\u200d'

# Common social media slang / abbreviation expansions for Banglish
BANGLISH_SLANG_MAP = {
    r'\bkno\b': 'keno',
    r'\bvlo\b': 'bhalo',
    r'\bblo\b': 'bhalo',
    r'\btnx\b': 'dhonnobad',
    r'\bthx\b': 'dhonnobad',
    r'\bplz\b': 'doya kore',
    r'\bpls\b': 'doya kore',
    r'\br\b': 'ar',
    r'\bu\b': 'tumi',
    r'\bur\b': 'tomar',
    r'\bwlc\b': 'shagotom',
    r'\bgd\b': 'bhalo',
}

def normalize_bangla(text: str) -> str:
    """
    Normalizes standard Bengali text:
    - Removes unnecessary Zero-Width Non-Joiner (ZWNJ) and Zero-Width Joiner (ZWJ)
    - Normalizes Bengali Dari (।) and removes duplicate punctuation (।। -> ।)
    - Collapses consecutive whitespace
    - Normalizes common nukta and hasanta compositions
    """
    if not text or not isinstance(text, str):
        return ""

    res = text

    # Remove rogue ZWNJ / ZWJ at word boundaries
    res = re.sub(r'[\u200B-\u200D\uFEFF]', '', res)

    # Normalize Dari (।) duplicates: '।।' -> '।'
    res = re.sub(r'।+', '।', res)

    # Normalize excessive punctuation (???? -> ?, !!!! -> !)
    res = re.sub(r'\?+', '?', res)
    res = re.sub(r'!+', '!', res)
    res = re.sub(r'\.+', '.', res)

    # Normalize spaces around punctuation
    res = re.sub(r'\s+([।,?!;:])', r'\1', res)
    res = re.sub(r'([।,?!;:])(?=[^\s।,?!;:])', r'\1 ', res)

    # Collapse multiple whitespaces
    res = re.sub(r'[ \t]+', ' ', res).strip()

    return res

def normalize_banglish(text: str) -> str:
    """
    Normalizes colloquial / social media Banglish text:
    - Collapses elongated character stretching:
      e.g. 'onekttttaaaa' -> 'onekta', 'haaaaiiii' -> 'hai', 'shuuuuunooo' -> 'shuno'
    - Expands SMS / texting slang: 'kno' -> 'keno', 'vlo' -> 'bhalo'
    - Cleans duplicate punctuation and whitespace
    """
    if not text or not isinstance(text, str):
        return ""

    res = text

    # Collapse characters repeated 3 or more times to 1 or 2 (e.g. 'sooo' -> 'so', 'naaaa' -> 'na')
    # Preserves legitimate double consonants like 'shobai' or 'accha'
    res = re.sub(r'([a-zA-Z])\1{2,}', r'\1', res)

    # Expand common Banglish abbreviations
    for pattern, rep in BANGLISH_SLANG_MAP.items():
        res = re.sub(pattern, rep, res, flags=re.IGNORECASE)

    # Normalize excessive punctuation
    res = re.sub(r'\?+', '?', res)
    res = re.sub(r'!+', '!', res)
    res = re.sub(r'\.+', '.', res)

    # Normalize spaces around punctuation
    res = re.sub(r'\s+([,?!;:])', r'\1', res)
    res = re.sub(r'([,?!;:])(?=[^\s,?!;:])', r'\1 ', res)

    # Collapse whitespace
    res = re.sub(r'\s+', ' ', res).strip()

    return res

def normalize_text(text: str) -> str:
    """
    Universal normalizer: Auto-detects whether text contains Bengali characters
    and applies the appropriate cleaning pipeline.
    """
    if not text or not isinstance(text, str):
        return ""

    has_bengali = bool(re.search(r'[\u0980-\u09FF]', text))
    if has_bengali:
        return normalize_bangla(text)
    else:
        return normalize_banglish(text)
