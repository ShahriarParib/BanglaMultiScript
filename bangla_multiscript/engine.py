# -*- coding: utf-8 -*-
"""
BanglaMultiScript Core Engine
Provides high-throughput, linguistically sound conversion from standard Bengali
to Natural Avro Banglish and Natural Code-Mixed text.
"""

import re
import unicodedata
from typing import List, Dict, Union, Optional

from .lexicon import (
    LOANWORDS_AND_ENTITIES,
    COLLOQUIAL_LEXICON,
    CODEMIXED_REPLACEMENTS,
    VOWELS_INDEP,
    VOWELS_DEP,
    CONSONANTS,
    CONJUNCT_MAP
)

def clean_repetition_trash(text: str) -> str:
    """
    Cleans up artificial repetition loops and trailing acronym spam
    common in machine translation outputs (e.g. 'si. es. si. es...').
    """
    if not text or not isinstance(text, str):
        return ""
    # Match identical short token (e.g. 'si. ' or 'es. ') repeated 3+ times
    cleaned = re.sub(r'(?:(\b[a-zA-Z\u0980-\u09FF]{1,4}\.?\s+)\1{2,})', r'\1', text)
    # Match 2-token phrase repeated 3+ times (e.g. 'si. es. si. es. si. es.')
    cleaned = re.sub(r'(?:(\b\w+\.?\s+\w+\.?\s+)\1{2,})', r'\1', cleaned)
    # Match any word repeated consecutively 3+ times
    cleaned = re.sub(r'\b(\w+)(?:\s+\1){2,}\b', r'\1', cleaned)
    # Clean trailing acronym loops (e.g. trailing 'সি. এস. সি. এস.')
    cleaned = re.sub(r'(?:[a-zA-Z\u0980-\u09FF]{1,3}\.\s*){4,}', ' ', cleaned)
    cleaned = re.sub(r'[,.\s]+$', '.', cleaned)
    return re.sub(r'\s+', ' ', cleaned).strip()

def phonological_word_to_banglish(word: str) -> str:
    """
    Transliterates a single Bengali token into natural Avro Banglish
    respecting inherent schwa vowel deletion, conjunct gemination, and common suffixes.
    """
    clean = re.sub(r'[^\w\u0980-\u09FF]', '', word)
    if not clean:
        return word
    
    # 1. Direct Colloquial Lexicon Lookup
    if clean in COLLOQUIAL_LEXICON:
        return COLLOQUIAL_LEXICON[clean]
    
    # 2. Suffix Decomposition
    for suffix, rep in [
        ('ের', 'er'), ('দের', 'der'), ('গুলো', 'gulo'), ('গুলি', 'guli'),
        ('কে', 'ke'), ('তে', 'te'), ('টা', 'ta'), ('টি', 'ti'),
        ('ভাবে', 'bhabe'), ('মূলক', 'mulok'), ('কারী', 'kari'), ('কারিদের', 'karider')
    ]:
        if clean.endswith(suffix) and len(clean) > len(suffix) + 1:
            stem = clean[:-len(suffix)]
            if stem in COLLOQUIAL_LEXICON:
                return COLLOQUIAL_LEXICON[stem] + ('-' if suffix in ['টা', 'টি'] else '') + rep
    
    # 3. Conjunct Resolution
    w = unicodedata.normalize('NFC', clean)
    for cj, rep in CONJUNCT_MAP.items():
        w = w.replace(cj, rep)
    
    # 4. Phonetic Traversal
    res = []
    i = 0
    n = len(w)
    while i < n:
        c = w[i]
        if i + 1 < n and w[i+1] == '়':
            c = c + '়'
            i += 1
            
        if c in VOWELS_INDEP:
            res.append(VOWELS_INDEP[c])
        elif c in CONSONANTS:
            res.append(CONSONANTS[c])
            if i + 1 < n:
                nxt = w[i+1]
                if nxt == '্':
                    i += 1  # Skip hasanta
                elif nxt in VOWELS_DEP:
                    res.append(VOWELS_DEP[nxt])
                    i += 1
                elif nxt in CONSONANTS or nxt in VOWELS_INDEP:
                    # Inherent vowel rule: insert 'o' between consonants
                    res.append('o')
        elif c in VOWELS_DEP:
            res.append(VOWELS_DEP[c])
        else:
            res.append(c)
        i += 1
        
    s = ''.join(res)
    # Clean double 'o' or unnatural clusters
    s = re.sub(r'oo+', 'o', s)
    s = re.sub(r'yy+', 'y', s)
    return s

def to_natural_banglish(text: str) -> str:
    """
    Converts a standard Bengali sentence into colloquial Avro Banglish.
    Preserves English loanwords, technical nomenclature, and entity names in proper Latin.
    """
    if not text or not isinstance(text, str):
        return ""
    
    # 1. Map known loanwords and entities
    res = text
    for bn_term, eng_term in LOANWORDS_AND_ENTITIES:
        pattern = re.escape(bn_term)
        res = re.sub(pattern, eng_term, res)
        
    # 2. Tokenize and convert remaining Bengali script tokens
    tokens = re.split(r'(\s+|[.,!?;:\"\'\(\)\[\]|।])', res)
    out = []
    for t in tokens:
        if not t:
            continue
        if re.search(r'[\u0980-\u09FF]', t):
            out.append(phonological_word_to_banglish(t))
        elif t == '।':
            out.append('.')
        else:
            out.append(t)
            
    final_text = ''.join(out)
    final_text = clean_repetition_trash(final_text)
    
    # Common post-cleanup heuristics
    final_text = re.sub(r'\bkno\b', 'keno', final_text, flags=re.IGNORECASE)
    final_text = re.sub(r'\bbaddhy\b', 'baddho', final_text, flags=re.IGNORECASE)
    final_text = re.sub(r'\bsmpork\b', 'shomporko', final_text, flags=re.IGNORECASE)
    final_text = re.sub(r'\bsmpourn\b', 'shompurno', final_text, flags=re.IGNORECASE)
    final_text = re.sub(r'\bchndrer\b', 'chondrer', final_text, flags=re.IGNORECASE)
    final_text = re.sub(r'\bchndro\b', 'chondro', final_text, flags=re.IGNORECASE)
    final_text = re.sub(r'\bkkhma\b', 'khoma', final_text, flags=re.IGNORECASE)
    final_text = re.sub(r'\bljjoa\b', 'lojja', final_text, flags=re.IGNORECASE)
    final_text = re.sub(r'\bodrishy\b', 'odrishyo', final_text, flags=re.IGNORECASE)
    final_text = re.sub(r'\bbouddhik\b', 'boudhik', final_text, flags=re.IGNORECASE)
    final_text = re.sub(r'\bsmbhoabybhabe\b', 'shombhabobhabe', final_text, flags=re.IGNORECASE)
    
    return re.sub(r'\s+', ' ', final_text).strip()

def to_natural_codemixed(text: str) -> str:
    """
    Transforms standard Bengali text into natural urban Code-Mixed Bengali-English.
    Replaces technical, conversational, and security concepts with authentic English loanwords
    while preserving Bengali morpho-syntax.
    """
    if not text or not isinstance(text, str):
        return ""
    res = text
    for pattern, rep in CODEMIXED_REPLACEMENTS:
        res = re.sub(pattern, rep, res)
    return clean_repetition_trash(res)

class MultiScriptConverter:
    """
    High-level class for converting Bengali text, batches, or DataFrames
    into multiple parallel scripts.
    """
    def __init__(self, cache_size: int = 10000, translator=None):
        self._cache = {}
        self.cache_size = cache_size
        self._translator = translator

    def convert_sentence(self, text: str, mode: str = 'all', src_lang: str = 'bn') -> Union[str, Dict[str, str]]:
        """
        Converts a single sentence.
        mode: 'banglish', 'codemixed', or 'all' (returns dict)
        src_lang: 'bn' (Bengali, default) or 'en' (English, translated first)
        """
        if not text or not isinstance(text, str):
            return "" if mode != 'all' else {'bangla': '', 'banglish': '', 'codemixed': ''}

        bn_text = text
        if src_lang == 'en':
            if self._translator is None:
                from .translator import get_translator
                self._translator = get_translator("auto")
            bn_text = self._translator.translate(text)

        if mode == 'banglish':
            return to_natural_banglish(bn_text)
        elif mode == 'codemixed':
            return to_natural_codemixed(bn_text)
        else:
            res = {
                'bangla': bn_text,
                'banglish': to_natural_banglish(bn_text),
                'codemixed': to_natural_codemixed(bn_text)
            }
            if src_lang == 'en':
                res['english'] = text
            return res

    def convert_batch(self, texts: List[str], mode: str = 'banglish', src_lang: str = 'bn') -> List[Union[str, Dict[str, str]]]:
        """Converts a list of sentences."""
        return [self.convert_sentence(t, mode=mode, src_lang=src_lang) for t in texts]

    def convert_dataframe(self, df, text_column: str,
                          banglish_col: str = 'text_banglish',
                          codemixed_col: str = 'text_codemixed'):
        """
        Takes a pandas DataFrame and adds natural Banglish and Code-Mixed columns in-place.
        """
        df[banglish_col] = df[text_column].apply(to_natural_banglish)
        df[codemixed_col] = df[text_column].apply(to_natural_codemixed)
        return df

def all_in_one(
    text: str,
    src_lang: str = "auto",
    translator_backend: str = "auto",
    translator_model_path: Optional[str] = None
) -> Dict[str, str]:
    """
    All-in-one unified converter.
    Accepts Bengali or English text and outputs all script representations:
    - Bengali (বাংলা)
    - Natural Avro Banglish
    - Modern Urban Code-Mixed
    - (English original if translated)

    Parameters:
        text (str): Input text in Bengali or English.
        src_lang (str): 'auto', 'bn', or 'en'.
        translator_backend (str): 'auto', 'web', 'indictrans2', or 'none'.
        translator_model_path (str, optional): Custom path or HuggingFace ID for IndicTrans2.
    """
    if not text or not isinstance(text, str):
        return {"bangla": "", "banglish": "", "codemixed": ""}

    is_english = False
    if src_lang == "en":
        is_english = True
    elif src_lang == "auto":
        # Detect if text contains Bengali Unicode characters (U+0980 to U+09FF)
        has_bengali = bool(re.search(r'[\u0980-\u09FF]', text))
        if not has_bengali and any(c.isalpha() for c in text):
            is_english = True

    if is_english and translator_backend != "none":
        from .translator import get_translator
        tr = get_translator(backend=translator_backend, model_path=translator_model_path)
        bn_text = tr.translate(text)
        return {
            "english": text,
            "bangla": bn_text,
            "banglish": to_natural_banglish(bn_text),
            "codemixed": to_natural_codemixed(bn_text)
        }
    else:
        return {
            "bangla": text,
            "banglish": to_natural_banglish(text),
            "codemixed": to_natural_codemixed(text)
        }

