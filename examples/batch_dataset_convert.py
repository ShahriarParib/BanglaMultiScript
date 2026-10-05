# -*- coding: utf-8 -*-
"""
Example: Batch Dataset Processing with BanglaMultiScript
Demonstrates how to take an English or Bengali DataFrame and convert it to 4 parallel scripts.
"""

import sys
import os
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.stdout.reconfigure(encoding='utf-8')

from bangla_multiscript import MultiScriptConverter

def main():
    print("=" * 75)
    print("Batch Dataset Processing with BanglaMultiScript")
    print("=" * 75)

    # 1. Create a dummy dataset
    sample_data = {
        "id": [1, 2, 3],
        "category": ["cyber_safety", "astronomy", "linguistics"],
        "prompt_bn": [
            "টু-ফ্যাক্টর অথেনটিকেশন (2FA) কীভাবে অনলাইন অ্যাকাউন্টের পাসওয়ার্ড রক্ষা করে?",
            "অ্যাপোলো 11 মিশনের সময় মহাকাশচারী নিল আর্মস্ট্রং চন্দ্রের কাঠামো প্রত্যক্ষ করছেন।",
            "বাংলা রূপক বাক্য 'চোখের বিষ' বলতে কী বোঝায়?"
        ]
    }

    df = pd.DataFrame(sample_data)
    print("Original DataFrame:")
    print(df[["id", "prompt_bn"]])

    # 2. Convert to Natural Banglish & Code-Mixed in-place
    conv = MultiScriptConverter()
    df_converted = conv.convert_dataframe(df, text_column="prompt_bn")

    print("\nConverted DataFrame (Multi-Script):")
    print(df_converted[["id", "prompt_bn", "text_banglish", "text_codemixed"]])

    # 3. Save to CSV / JSONL
    out_csv = "sample_multiscript_output.csv"
    df_converted.to_csv(out_csv, index=False, encoding="utf-8")
    print(f"\nSaved multi-script dataset to {out_csv}!")

    if os.path.exists(out_csv):
        os.remove(out_csv)

if __name__ == "__main__":
    main()
