# -*- coding: utf-8 -*-
"""
BanglaMultiScript Modular Translation Engine
Provides English-to-Bengali translation backends (IndicTrans2, Hugging Face NLLB, Google/Web, Custom).
"""

import os
import sys
import time
from typing import List, Union, Optional, Callable

class BaseTranslator:
    def translate(self, text: str) -> str:
        raise NotImplementedError
        
    def translate_batch(self, texts: List[str]) -> List[str]:
        return [self.translate(t) for t in texts]

class IndicTrans2Translator(BaseTranslator):
    """
    Offline neural translation using AI4Bharat's IndicTrans2 model.
    Runs locally on CPU or GPU without external API limits.
    """
    def __init__(self, model_dir_or_name: str = "d:\\Dataset Creation\\indictrans2_model", device: str = "cpu"):
        self.device = device
        self.model_path = model_dir_or_name
        self.model = None
        self.tokenizer = None
        self.ip = None
        self._loaded = False

    def _lazy_load(self):
        if self._loaded:
            return
        import torch
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        from IndicTransToolkit.processor import IndicProcessor
        
        self.ip = IndicProcessor(inference=True)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_path, trust_remote_code=True)
        self.model.to(self.device)
        self.model.eval()
        self._loaded = True

    def translate(self, text: str) -> str:
        if not text or not str(text).strip():
            return ""
        return self.translate_batch([text])[0]

    def translate_batch(self, texts: List[str], batch_size: int = 16) -> List[str]:
        self._lazy_load()
        import torch
        results = []
        for i in range(0, len(texts), batch_size):
            sub = [t if str(t).strip() else "N/A" for t in texts[i:i+batch_size]]
            preprocessed = self.ip.preprocess_batch(sub, src_lang="eng_Latn", tgt_lang="ben_Beng")
            inputs = self.tokenizer(preprocessed, truncation=True, padding="longest", return_tensors="pt").to(self.device)
            with torch.no_grad():
                outputs = self.model.generate(**inputs, max_length=384, num_beams=1)
            with self.tokenizer.as_target_tokenizer():
                decoded = self.tokenizer.batch_decode(outputs.detach().cpu().tolist(), skip_special_tokens=True)
            results.extend(self.ip.postprocess_batch(decoded, lang="ben_Beng"))
        return results

class WebTranslator(BaseTranslator):
    """
    Lightweight web translation fallback (no model download required).
    """
    def __init__(self):
        pass

    def translate(self, text: str) -> str:
        if not text or not str(text).strip():
            return ""
        try:
            from deep_translator import GoogleTranslator
            return GoogleTranslator(source='en', target='bn').translate(text)
        except Exception:
            try:
                from deep_translator import MyMemoryTranslator
                return MyMemoryTranslator(source='en', target='bn').translate(text)
            except Exception as e:
                return text

    def translate_batch(self, texts: List[str]) -> List[str]:
        return [self.translate(t) for t in texts]

class CustomTranslator(BaseTranslator):
    """Wraps any user-supplied translation function."""
    def __init__(self, func: Callable[[str], str]):
        self.func = func

    def translate(self, text: str) -> str:
        return self.func(text)

    def translate_batch(self, texts: List[str]) -> List[str]:
        return [self.func(t) for t in texts]

def get_translator(backend: str = "auto", model_path: Optional[str] = None) -> BaseTranslator:
    """
    Factory function to get the appropriate translation backend.
    backend: 'indictrans2', 'web', 'auto', or 'none'
    """
    if backend == "indictrans2":
        path = model_path or (r"d:\Dataset Creation\indictrans2_model" if os.path.exists(r"d:\Dataset Creation\indictrans2_model") else "ai4bharat/indictrans2-en-indic-1B")
        return IndicTrans2Translator(model_dir_or_name=path)
    elif backend == "web":
        return WebTranslator()
    elif backend == "auto":
        if os.path.exists(r"d:\Dataset Creation\indictrans2_model"):
            return IndicTrans2Translator(model_dir_or_name=r"d:\Dataset Creation\indictrans2_model")
        return WebTranslator()
    else:
        return WebTranslator()
