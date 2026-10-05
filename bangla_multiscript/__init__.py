# -*- coding: utf-8 -*-
"""
BanglaMultiScript: High-Throughput Bengali to Natural Avro Banglish & Code-Mixed Alignment Engine.
"""

__version__ = "1.0.0"
__author__ = "Shahriar"

from .engine import (
    to_natural_banglish,
    to_natural_codemixed,
    clean_repetition_trash,
    phonological_word_to_banglish,
    MultiScriptConverter,
    all_in_one
)
from .translator import IndicTrans2Translator, WebTranslator, CustomTranslator, get_translator
from .detector import detect_script, get_script_stats
from .normalizer import normalize_bangla, normalize_banglish, normalize_text
from .exporter import export_to_sharegpt, export_to_alpaca, export_to_dpo
from .ui import launch_ui

__all__ = [
    # Core Engine
    "to_natural_banglish",
    "to_natural_codemixed",
    "clean_repetition_trash",
    "phonological_word_to_banglish",
    "MultiScriptConverter",
    "all_in_one",
    # Translation
    "IndicTrans2Translator",
    "WebTranslator",
    "CustomTranslator",
    "get_translator",
    # Script Detection
    "detect_script",
    "get_script_stats",
    # Text Normalization
    "normalize_bangla",
    "normalize_banglish",
    "normalize_text",
    # LLM Dataset Exporters
    "export_to_sharegpt",
    "export_to_alpaca",
    "export_to_dpo",
    # Web UI
    "launch_ui",
    # Metadata
    "__version__",
]

