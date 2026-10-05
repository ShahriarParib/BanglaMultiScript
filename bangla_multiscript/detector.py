# -*- coding: utf-8 -*-
"""
BanglaMultiScript Script & Language Identification (LID) Module
Detects whether a given text is Bengali, Avro Banglish, English, or Code-Mixed.
"""

import re
from typing import Dict, Union

# Common Banglish grammatical particles and high-frequency phonetic markers
BANGLISH_MARKERS = {
    "ami", "tumi", "apni", "amra", "tomra", "apnara", "she", "tini", "tara",
    "kemon", "achi", "achho", "achhen", "bhalo", "valo", "korcho", "korchhi",
    "korben", "korte", "hobe", "hobena", "hoy", "hoyeche", "hoyechhe",
    "keno", "kintu", "ebong", "ar", "aar", "aaroo", "aro", "kothay", "kokhon",
    "kivabe", "ki", "kee", "shob", "sob", "thik", "ekhon", "tokhon",
    "gotokal", "aaj", "ajke", "shathe", "sathe", "theke", "por", "pore",
    "jani", "janina", "dekhi", "dekhun", "bolun", "bolte", "shunte",
    "parbo", "parbena", "parbe", "uchit", "chilo", "chhilo", "achhe",
    "eta", "ota", "ei", "oi", "ekta", "duita", "shunte", "bujhte",
    "darao", "ashbo", "jabo", "korechi", "gesilam", "giyechilam"
}

# Common English stopwords
ENGLISH_MARKERS = {
    "the", "is", "are", "was", "were", "and", "or", "but", "if", "then",
    "what", "why", "how", "when", "where", "who", "which", "this", "that",
    "these", "those", "have", "has", "had", "will", "would", "shall",
    "should", "can", "could", "may", "might", "must", "with", "from",
    "about", "against", "between", "into", "through", "during", "before",
    "after", "above", "below", "to", "of", "for", "in", "on", "at", "by"
}

def get_script_stats(text: str) -> Dict[str, float]:
    """
    Computes character-level distribution across scripts:
    Returns percentages of Bengali, Latin, Digits, and Punctuation/Whitespace.
    """
    if not text or not isinstance(text, str):
        return {"bengali": 0.0, "latin": 0.0, "digits": 0.0, "other": 0.0, "total_chars": 0}

    total = len(text)
    bn_count = len(re.findall(r'[\u0980-\u09FF]', text))
    latin_count = len(re.findall(r'[a-zA-Z]', text))
    digit_count = len(re.findall(r'[0-9\u09E6-\u09EF]', text))
    other_count = total - (bn_count + latin_count + digit_count)

    return {
        "bengali": round(bn_count / total, 4),
        "latin": round(latin_count / total, 4),
        "digits": round(digit_count / total, 4),
        "other": round(other_count / total, 4),
        "total_chars": total
    }

def detect_script(text: str) -> str:
    """
    Detects the predominant script / language form of the text:
    - 'bengali': Formal Bengali script (বাংলা)
    - 'banglish': Bengali written using English / Latin letters (Avro Banglish)
    - 'codemixed': Sentence containing significant blend of Bengali and English words
    - 'english': Standard English text
    - 'unknown': Empty or numeric/symbol-only text
    """
    if not text or not isinstance(text, str):
        return "unknown"

    stats = get_script_stats(text)
    bn_ratio = stats["bengali"]
    latin_ratio = stats["latin"]

    # If virtually no alphabetic characters
    if bn_ratio == 0 and latin_ratio == 0:
        return "unknown"

    # Both Bengali and Latin present in meaningful amounts -> Code-Mixed
    if bn_ratio >= 0.15 and latin_ratio >= 0.15:
        return "codemixed"

    # Predominantly Bengali script
    if bn_ratio > 0.40 and latin_ratio < 0.15:
        return "bengali"

    # Predominantly Latin characters -> Distinguish Banglish vs English
    tokens = [re.sub(r'[^a-zA-Z]', '', w).lower() for w in text.split()]
    tokens = [w for w in tokens if len(w) > 1]

    if not tokens:
        return "unknown"

    banglish_score = sum(1 for t in tokens if t in BANGLISH_MARKERS)
    english_score = sum(1 for t in tokens if t in ENGLISH_MARKERS)

    # If Banglish marker hits exist and exceed English
    if banglish_score > english_score:
        return "banglish"
    elif english_score > banglish_score:
        return "english"

    # Secondary heuristic: phonetic character combinations typical in Banglish
    # (e.g. 'kh', 'gh', 'ch', 'jh', 'th', 'dh', 'bh', 'sh', 'ng', 'chho')
    banglish_phonetic_pattern = re.compile(r'(chho|kkh|sh|bh|dh|th|jh|ch|gh|kh|ng|oy|ye)')
    phonetic_hits = len(banglish_phonetic_pattern.findall(text.lower()))
    word_count = len(tokens)

    if word_count > 0 and (phonetic_hits / word_count) >= 0.6:
        return "banglish"

    # Fallback based on dominant character ratio
    if bn_ratio > latin_ratio:
        return "bengali"
    return "english"
