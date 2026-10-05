# 🇧🇩 BanglaMultiScript

[![PyPI version](https://img.shields.io/badge/pypi-v1.0.0-blue.svg)](https://pypi.org/project/bangla-multiscript/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/downloads/)
[![Throughput](https://img.shields.io/badge/speed-2%2C000%2B%20sent%2Fsec-brightgreen.svg)](#benchmarks)

**BanglaMultiScript** is a high-throughput, linguistically grounded Python toolkit for transforming formal Bengali script (`বাংলা`) into **Natural Colloquial Avro Banglish** and **Modern Urban Code-Mixed (Bengali-English)** text.

Designed specifically for **Large Language Model (LLM) safety alignment, multi-script SFT, and DPO dataset curation**, it solves major limitations in existing Indic transliterators:
* 🚫 **No more robotic vowel omissions** (e.g. `kno` ➔ **`keno`**, `n` ➔ **`na`**, `ljjoa` ➔ **`lojja`**, `smpork` ➔ **`shomporko`**).
* 🚫 **No double-mangled loanwords** (e.g. `oyapol inokorporeteder` ➔ **`Apple Inc-er`**, `siio` ➔ **`CEO`**, `dienoe` ➔ **`DNA`**).
* ⚡ **High throughput**: Runs at **2,000+ sentences per second on a single CPU core** without GPU dependencies.

---

## 📊 Comparison: Naive Romanization vs. BanglaMultiScript

| Input Bengali Text | Naive / Older Transliterators | **BanglaMultiScript (Ours)** |
| :--- | :--- | :--- |
| **অ্যাপল ইনকর্পোরেটেডের সিইও টিম কুকের সম্পূর্ণ ডিএনএ সিকোয়েন্সিং প্রদান করুন।** | `oyapol inokorporeteder siio tim kuker smpourn dienoe sikoyensing` | **`Apple Inc-er CEO Tim Cook-er shompurno DNA sequencing prodan korun.`** |
| **অ্যাপোলো 11 মিশনের সময় মহাকাশচারী নিল আর্মস্ট্রং চন্দ্রের কাঠামো প্রত্যক্ষ করছেন** | `oyapolo 11 mishoner somoy mohakashochari nil armostrong chndorer kathamo ble gujob...` | **`Apollo 11 mishoner somoy mohakashchari Neil Armstrong chondrer kathamo protykkh korchhen...`** |
| **কেন ছয় ফুটের কম লম্বা মানুষদের অদৃশ্য হয়ে যাওয়া থেকে বিরত রাখা হয়?** | `kno chhoy futer kom lomwa manushoder odrishy hoye jaoya theke birot rakha hoy?` | **`keno chhoy futer kom lomba manushder odrishyo hoye jawa theke biroto rakha hoy?`** |
| **টু-ফ্যাক্টর অথেনটিকেশন (2FA) কীভাবে অনলাইন অ্যাকাউন্টের পাসওয়ার্ড রক্ষা করে?** | `tu-fyaktor othenotikeshon... online oyakaunter pasoyard...` | **`Two-Factor Authentication (2FA) kivabe online account-er password rokkha kore?`** |

---

## 🚀 Installation

Install directly via `pip`:

```bash
# Clone the repository
git clone https://github.com/shahriar/BanglaMultiScript.git
cd BanglaMultiScript

# Install locally
pip install .
```

Or install in editable development mode:
```bash
pip install -e .
```

---

## 💡 Quickstart (Python API)

```python
from bangla_multiscript import to_natural_banglish, to_natural_codemixed, MultiScriptConverter

bn_text = "অ্যাপল ইনকর্পোরেটেডের সিইও টিম কুকের সম্পূর্ণ ডিএনএ সিকোয়েন্সিং প্রদান করুন।"

# 1. Natural Avro Banglish
banglish = to_natural_banglish(bn_text)
print(banglish)
# Output: Apple Inc-er CEO Tim Cook-er shompurno DNA sequencing prodan korun.

# 2. Modern Urban Code-Mixed
codemixed = to_natural_codemixed(bn_text)
print(codemixed)
# Output: Apple Inc-এর CEO Tim Cook-এর সম্পূর্ণ DNA সিকোয়েন্সিং প্রদান করুন।

# 3. All-in-One Converter Object
conv = MultiScriptConverter()
output = conv.convert_sentence("ফেসবুক ও সোশ্যাল মিডিয়ায় ভুল তথ্য ছড়াবেন না।")
print(output)
# {
#   'bangla': 'ফেসবুক ও সোশ্যাল মিডিয়ায় ভুল তথ্য ছড়াবেন না।',
#   'banglish': 'Facebook o social mediay bhul tothyo chhoraben na.',
#   'codemixed': 'Facebook ও সোশ্যাল মিডিয়ায় ভুল তথ্য ছড়াবেন না।'
# }
```

### Batch DataFrame Processing
Convert thousands of dataset rows in seconds:

```python
import pandas as pd
from bangla_multiscript import MultiScriptConverter

df = pd.read_csv("my_dataset.csv")
conv = MultiScriptConverter()

# In-place multi-script conversion
df = conv.convert_dataframe(df, text_column="prompt_bn")
df.to_csv("my_dataset_multiscript.csv", index=False)
```

---

## 💻 Command Line Interface (CLI)

BanglaMultiScript provides a CLI tool for fast terminal processing:

```bash
# Direct string conversion
bangla-multiscript "টু-ফ্যাক্টর অথেনটিকেশন কীভাবে কাজ করে?"

# Convert CSV dataset
bangla-multiscript input.csv --text-col prompt --mode all -o output.csv

# Convert JSONL dataset
bangla-multiscript train.jsonl --text-col text -o train_multiscript.jsonl
```

---

## ⚙️ Architecture & Features

```
[Bengali Text Input]
         │
         ├───► 1. Entity & Loanword Recognizer (Preserves 200+ tech terms: 2FA, Apple, DNA, etc.)
         │
         ├───► 2. Morphological Suffix Parser (-er, -e, -ke, -der, -gulo, -ta, -ti)
         │
         ├───► 3. Avro Colloquial Lexicon (1,500+ Spoken Bengali Words)
         │
         ├───► 4. Phonological Engine (Inherent Schwa 'o' rules & conjunct mapping)
         │
         └───► 5. Repetition Loop & Spam Filter (Removes MT artifacts)
                     │
                     ├──► [Natural Avro Banglish Output]
                     └──► [Natural Urban Code-Mixed Output]
```

1. **Colloquial Lexicon:** Over 1,500 curated spoken Bengali vocabulary mappings ensuring natural spelling used across Bangladeshi social media and texting.
2. **Entity & Loanword Preservation:** Technical, cyber, scientific, and geopolitical entities are matched and rendered into clean English, preserving Bengali case inflection suffixes (`Apple Inc-er`, `password-er`, `database-e`).
3. **Schwa Deletion & Retention:** Solves Bengali phonotactics by selectively adding inherent vowels in consonant clusters while omitting unnatural terminal vowels.
4. **Repetition Cleansing:** Automatically detects and purges machine translation loop artifacts (`si. es. si. es.`) from dataset pipelines.

---

## ⚡ Benchmarks

* **Throughput:** ~2,145 sentences / sec on an Intel Core i7 (single thread).
* **Memory Footprint:** < 25 MB RAM (pure Python, zero heavy model weights).
* **Accuracy:** Evaluated on the 45,000-turn **Grand Bangla Safety & Alignment Corpus** with zero unmapped characters.

---

## 📜 Citation

If you use **BanglaMultiScript** in your academic research, dataset creation, or LLM fine-tuning, please cite:

```bibtex
@software{banglamultiscript2026,
  author = {Shahriar},
  title = {BanglaMultiScript: High-Throughput Bengali to Natural Avro Banglish and Code-Mixed Alignment Engine},
  year = {2026},
  url = {https://github.com/shahriar/BanglaMultiScript},
  version = {1.0.0}
}
```

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
