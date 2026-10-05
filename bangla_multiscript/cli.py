# -*- coding: utf-8 -*-
"""
Command Line Interface for BanglaMultiScript
"""

import argparse
import sys
import os
import json

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from .engine import to_natural_banglish, to_natural_codemixed, MultiScriptConverter

def main():
    parser = argparse.ArgumentParser(
        description="BanglaMultiScript: Convert Bengali text to Natural Avro Banglish & Urban Code-Mixed."
    )
    parser.add_argument("input", nargs="?", help="Input string or path to a text/CSV/JSONL file.")
    parser.add_argument(
        "--mode", choices=["banglish", "codemixed", "all"], default="all",
        help="Conversion mode (default: all)"
    )
    parser.add_argument("--output", "-o", help="Output file path (optional).")
    parser.add_argument("--text-col", default="text", help="Text column name for CSV/JSONL input.")
    parser.add_argument("--ui", action="store_true", help="Launch the interactive Web UI studio in browser.")
    parser.add_argument("--port", type=int, default=7860, help="Port for the Web UI studio (default: 7860).")
    parser.add_argument("--detect", action="store_true", help="Detect script/language (bengali, banglish, english, codemixed).")
    parser.add_argument("--normalize", action="store_true", help="Normalize and clean text (remove ZWNJ, slang, letter stretching).")

    args = parser.parse_args()

    if args.ui:
        from .ui import launch_ui
        launch_ui(port=args.port)
        return

    if not args.input:
        parser.print_help()
        sys.exit(0)

    if args.detect:
        from .detector import detect_script
        print(detect_script(args.input))
        return

    if args.normalize:
        from .normalizer import normalize_text
        print(normalize_text(args.input))
        return

    # Check if input is a file
    if os.path.isfile(args.input):
        ext = os.path.splitext(args.input)[1].lower()
        if ext == '.csv':
            import pandas as pd
            df = pd.read_csv(args.input)
            conv = MultiScriptConverter()
            df = conv.convert_dataframe(df, text_column=args.text_col)
            out_path = args.output or args.input.replace('.csv', '_multiscript.csv')
            df.to_csv(out_path, index=False, encoding='utf-8')
            print(f"Saved converted CSV ({len(df)} rows) to: {out_path}")
        elif ext == '.jsonl':
            out_path = args.output or args.input.replace('.jsonl', '_multiscript.jsonl')
            count = 0
            with open(args.input, 'r', encoding='utf-8') as fin, open(out_path, 'w', encoding='utf-8') as fout:
                for line in fin:
                    d = json.loads(line)
                    raw_text = d.get(args.text_col, '')
                    d[f'{args.text_col}_banglish'] = to_natural_banglish(raw_text)
                    d[f'{args.text_col}_codemixed'] = to_natural_codemixed(raw_text)
                    fout.write(json.dumps(d, ensure_ascii=False) + '\n')
                    count += 1
            print(f"Saved converted JSONL ({count} records) to: {out_path}")
        else:
            # Plain text file line by line
            out_path = args.output or args.input + '.converted'
            with open(args.input, 'r', encoding='utf-8') as fin, open(out_path, 'w', encoding='utf-8') as fout:
                for line in fin:
                    if args.mode == 'banglish':
                        fout.write(to_natural_banglish(line.strip()) + '\n')
                    elif args.mode == 'codemixed':
                        fout.write(to_natural_codemixed(line.strip()) + '\n')
                    else:
                        res = {
                            'bn': line.strip(),
                            'banglish': to_natural_banglish(line.strip()),
                            'codemixed': to_natural_codemixed(line.strip())
                        }
                        fout.write(json.dumps(res, ensure_ascii=False) + '\n')
            print(f"Saved output to: {out_path}")
    else:
        # Input is a direct string
        if args.mode == 'banglish':
            print(to_natural_banglish(args.input))
        elif args.mode == 'codemixed':
            print(to_natural_codemixed(args.input))
        else:
            print("--- Original Bangla ---")
            print(args.input)
            print("\n--- Natural Avro Banglish ---")
            print(to_natural_banglish(args.input))
            print("\n--- Natural Code-Mixed ---")
            print(to_natural_codemixed(args.input))

if __name__ == "__main__":
    main()
