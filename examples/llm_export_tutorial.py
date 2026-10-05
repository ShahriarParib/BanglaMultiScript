import sys

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import pandas as pd
from bangla_multiscript import (
    MultiScriptConverter,
    detect_script,
    normalize_text,
    export_to_sharegpt,
    export_to_alpaca,
    export_to_dpo
)

def main():
    print("=" * 60)
    print("[BanglaMultiScript] LLM Alignment & Export Tutorial")
    print("=" * 60)

    # Sample raw Bengali dataset
    raw_data = [
        {
            "prompt": "কৃত্রিম বুদ্ধিমত্তা কীভাবে স্বাস্থ্যসেবায় সাহায্য করতে পারে?",
            "response": "AI বা কৃত্রিম বুদ্ধিমত্তা রোগ নির্ণয় এবং ড্রাগ ডিসকভারিতে সহায়তা করে।"
        },
        {
            "prompt": "সাইবার আক্রমণ থেকে নিজের কম্পিউটার সুরক্ষিত রাখার উপায় কী?",
            "response": "টু-ফ্যাক্টর অথেনটিকেশন (2FA) এবং স্ট্রং পাসওয়ার্ড ব্যবহার করা উচিত।"
        }
    ]
    df = pd.DataFrame(raw_data)

    print("\n[1] Multi-Script Conversion (Bangla -> Banglish & Code-Mixed):")
    conv = MultiScriptConverter()
    df["prompt_banglish"] = df["prompt"].apply(lambda x: conv.convert_sentence(x, mode="banglish"))
    df["response_banglish"] = df["response"].apply(lambda x: conv.convert_sentence(x, mode="banglish"))
    print(df[["prompt_banglish", "response_banglish"]])

    print("\n[2] Exporting to ShareGPT format for Unsloth / LLaMA-Factory:")
    sharegpt = export_to_sharegpt(
        df,
        prompt_col="prompt_banglish",
        response_col="response_banglish",
        system_prompt="You are an empathetic Bengali AI assistant communicating in natural Avro Banglish."
    )
    print(f"Sample ShareGPT record:\n{sharegpt[0]}")

    print("\n[3] Exporting to Alpaca format:")
    alpaca = export_to_alpaca(df, instruction_col="prompt", output_col="response")
    print(f"Sample Alpaca record:\n{alpaca[0]}")

    print("\n✅ LLM Dataset Export completed successfully!")

if __name__ == "__main__":
    main()
