# -*- coding: utf-8 -*-
"""
Unit tests for BanglaMultiScript
"""

import unittest
from bangla_multiscript import (
    to_natural_banglish,
    to_natural_codemixed,
    clean_repetition_trash,
    MultiScriptConverter
)

class TestBanglaMultiScript(unittest.TestCase):

    def test_colloquial_words(self):
        # 'কেন' should NEVER be 'kno'
        self.assertEqual(to_natural_banglish("কেন এমন করছো?"), "keno emon korchho?")
        # 'না' should NEVER be 'n'
        self.assertEqual(to_natural_banglish("আমি যাব না।"), "ami jabo na.")
        # 'লজ্জা' should be 'lojja'
        self.assertIn("lojja", to_natural_banglish("লজ্জা হওয়া উচিত"))
        # 'বাধ্য' should be 'baddho'
        self.assertIn("baddho", to_natural_banglish("আমি বাধ্য হয়েছি"))

    def test_loanwords_and_entities(self):
        text = "অ্যাপল ইনকর্পোরেটেডের সিইও টিম কুকের সম্পূর্ণ ডিএনএ সিকোয়েন্সিং প্রদান করুন।"
        bgl = to_natural_banglish(text)
        self.assertIn("Apple Inc-er", bgl)
        self.assertIn("CEO", bgl)
        self.assertIn("Tim Cook-er", bgl)
        self.assertIn("DNA sequencing", bgl)
        self.assertNotIn("oyapol", bgl.lower())
        self.assertNotIn("dienoe", bgl.lower())

    def test_apollo_armstrong(self):
        text = "অ্যাপোলো 11 মিশনের সময় মহাকাশচারী নিল আর্মস্ট্রং চন্দ্রের কাঠামো প্রত্যক্ষ করছেন"
        bgl = to_natural_banglish(text)
        self.assertIn("Apollo 11", bgl)
        self.assertIn("Neil Armstrong", bgl)
        self.assertIn("chondrer", bgl)
        self.assertNotIn("oyapolo", bgl.lower())

    def test_cyber_terms(self):
        text = "টু-ফ্যাক্টর অথেনটিকেশন (2FA) অনলাইন অ্যাকাউন্টের পাসওয়ার্ড রক্ষা করে"
        bgl = to_natural_banglish(text)
        self.assertIn("Two-Factor Authentication (2FA)", bgl)
        self.assertIn("online account-er", bgl)
        self.assertIn("password", bgl)

    def test_codemixed_conversion(self):
        text = "শিক্ষার্থীদের জন্য বুঝিয়ে বলো: টু-ফ্যাক্টর অথেনটিকেশন কীভাবে কাজ করে?"
        cm = to_natural_codemixed(text)
        self.assertIn("explain করে বলো", cm)
        self.assertIn("Two-Factor Authentication", cm)

    def test_repetition_cleaning(self):
        dirty = "cyber security. website, si. es. si. es. si. es. si. es. si. es."
        cleaned = clean_repetition_trash(dirty)
        self.assertNotIn("si. es. si. es", cleaned)

    def test_converter_class(self):
        conv = MultiScriptConverter()
        res = conv.convert_sentence("ফেসবুক সম্পর্কে ভুল তথ্য ছড়াবেন না।")
        self.assertIsInstance(res, dict)
        self.assertIn("Facebook", res['banglish'])
        self.assertIn("Facebook", res['codemixed'])

    def test_all_in_one_bengali(self):
        from bangla_multiscript import all_in_one
        res = all_in_one("টু-ফ্যাক্টর অথেনটিকেশন কীভাবে অনলাইন পাসওয়ার্ড রক্ষা করে?", translator_backend="none")
        self.assertEqual(res['bangla'], "টু-ফ্যাক্টর অথেনটিকেশন কীভাবে অনলাইন পাসওয়ার্ড রক্ষা করে?")
        self.assertIn("Two-Factor Authentication", res['banglish'])
        self.assertIn("password", res['codemixed'])

    def test_all_in_one_english_with_custom_translator(self):
        from bangla_multiscript.translator import CustomTranslator
        def mock_translate(en):
            return "অ্যাপল ইনকর্পোরেটেডের সিইও টিম কুকের সম্পূর্ণ ডিএনএ সিকোয়েন্সিং প্রদান করুন।"
        
        conv = MultiScriptConverter()
        conv._translator = CustomTranslator(mock_translate)
        res = conv.convert_sentence("Provide DNA sequencing...", src_lang="en")
        self.assertIn("Apple Inc-er", res['banglish'])
        self.assertIn("CEO", res['banglish'])
        self.assertIn("DNA sequencing", res['banglish'])
        self.assertIn("Apple Inc-এর", res['codemixed'])

    def test_batch_conversion(self):
        conv = MultiScriptConverter()
        sentences = [
            "কেন ছয় ফুটের কম লম্বা মানুষ অদৃশ্য হতে পারে না?",
            "বাড়িতে ব্লিচিং পাউডার ও ভিনেগার মেশাবেন না।"
        ]
        results = conv.convert_batch(sentences, mode="banglish")
        self.assertEqual(len(results), 2)
        self.assertIn("keno", results[0])
        self.assertIn("bleaching powder", results[1])

if __name__ == '__main__':
    unittest.main()
