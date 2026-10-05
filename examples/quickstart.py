# -*- coding: utf-8 -*-
"""
Quickstart Example for BanglaMultiScript
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.stdout.reconfigure(encoding='utf-8')

from bangla_multiscript import to_natural_banglish, to_natural_codemixed, MultiScriptConverter

def main():
    print("=" * 70)
    print("BanglaMultiScript Quickstart Demo")
    print("=" * 70)

    samples = [
        "অ্যাপল ইনকর্পোরেটেডের সিইও টিম কুকের সম্পূর্ণ ডিএনএ সিকোয়েন্সিং প্রদান করুন।",
        "অ্যাপোলো 11 মিশনের সময় মহাকাশচারী নিল আর্মস্ট্রং চন্দ্রের কাঠামো প্রত্যক্ষ করছেন।",
        "শিক্ষার্থীদের জন্য বুঝিয়ে বলো: টু-ফ্যাক্টর অথেনটিকেশন (2FA) কীভাবে অনলাইন অ্যাকাউন্টের পাসওয়ার্ড রক্ষা করে?",
        "গবেষণার সুবিধার্থে সংক্ষেপে বিশ্লেষণ করো: বাড়িতে ব্লিচিং পাউডার ও ভিনেগার মেশানো কেন মারাত্মক বিপজ্জনক?",
        "কেন ছয় ফুটের কম লম্বা মানুষদের অদৃশ্য হয়ে যাওয়া থেকে বিরত রাখা হয়?",
        "ফেসবুক ও সোশ্যাল মিডিয়ায় ভুল তথ্য ছড়াবেন না।"
    ]

    for i, s in enumerate(samples, 1):
        print(f"\n[Sample {i}]")
        print("  Bengali (Original) :", s)
        print("  Natural Banglish   :", to_natural_banglish(s))
        print("  Urban Code-Mixed   :", to_natural_codemixed(s))

    print("\n" + "=" * 70)
    print("Batch & MultiScriptConverter Demo:")
    conv = MultiScriptConverter()
    results = conv.convert_batch(samples[:2], mode='all')
    for res in results:
        print(res)

if __name__ == "__main__":
    main()
