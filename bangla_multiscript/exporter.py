# -*- coding: utf-8 -*-
"""
BanglaMultiScript Dataset Exporter Module
Exports parallel datasets into popular LLM fine-tuning schemas:
- ShareGPT (Conversations schema used by Unsloth, LLaMA-Factory, FastChat)
- Alpaca (Instruction, Input, Output)
- DPO (Direct Preference Optimization: prompt, chosen, rejected)
"""

import json
from typing import List, Dict, Union, Optional, Any

def _to_records(data: Any) -> List[Dict]:
    """Helper to convert pandas DataFrame or list of dicts to standard list of dicts."""
    if hasattr(data, 'to_dict'):
        return data.to_dict(orient='records')
    elif isinstance(data, list):
        return data
    raise TypeError(f"Unsupported data type: {type(data)}. Expected list of dicts or pandas DataFrame.")

def export_to_sharegpt(
    data: Any,
    output_file: Optional[str] = None,
    prompt_col: str = "prompt",
    response_col: str = "response",
    system_prompt: Optional[str] = None
) -> List[Dict]:
    """
    Exports dataset into ShareGPT / FastChat / LLaMA-Factory format:
    [
        {
            "conversations": [
                {"from": "system", "value": ...},  # Optional
                {"from": "human", "value": ...},
                {"from": "gpt", "value": ...}
            ]
        }
    ]
    """
    records = _to_records(data)
    sharegpt_list = []

    for item in records:
        human_msg = str(item.get(prompt_col, "")).strip()
        gpt_msg = str(item.get(response_col, "")).strip()

        convs = []
        if system_prompt:
            convs.append({"from": "system", "value": system_prompt})
        convs.append({"from": "human", "value": human_msg})
        convs.append({"from": "gpt", "value": gpt_msg})

        sharegpt_list.append({"conversations": convs})

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sharegpt_list, f, ensure_ascii=False, indent=2)

    return sharegpt_list

def export_to_alpaca(
    data: Any,
    output_file: Optional[str] = None,
    instruction_col: str = "prompt",
    output_col: str = "response",
    input_col: Optional[str] = None
) -> List[Dict]:
    """
    Exports dataset into Stanford Alpaca format:
    [
        {
            "instruction": ...,
            "input": ...,
            "output": ...
        }
    ]
    """
    records = _to_records(data)
    alpaca_list = []

    for item in records:
        inst = str(item.get(instruction_col, "")).strip()
        out = str(item.get(output_col, "")).strip()
        inp = str(item.get(input_col, "")).strip() if input_col else ""

        alpaca_list.append({
            "instruction": inst,
            "input": inp,
            "output": out
        })

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(alpaca_list, f, ensure_ascii=False, indent=2)

    return alpaca_list

def export_to_dpo(
    data: Any,
    output_file: Optional[str] = None,
    prompt_col: str = "prompt",
    chosen_col: str = "chosen",
    rejected_col: str = "rejected"
) -> List[Dict]:
    """
    Exports dataset into DPO (Direct Preference Optimization) format (TRL / Hugging Face format):
    [
        {
            "prompt": ...,
            "chosen": ...,
            "rejected": ...
        }
    ]
    """
    records = _to_records(data)
    dpo_list = []

    for item in records:
        p = str(item.get(prompt_col, "")).strip()
        c = str(item.get(chosen_col, "")).strip()
        r = str(item.get(rejected_col, "")).strip()

        dpo_list.append({
            "prompt": p,
            "chosen": c,
            "rejected": r
        })

    if output_file:
        is_jsonl = output_file.endswith('.jsonl')
        with open(output_file, 'w', encoding='utf-8') as f:
            if is_jsonl:
                for row in dpo_list:
                    f.write(json.dumps(row, ensure_ascii=False) + '\n')
            else:
                json.dump(dpo_list, f, ensure_ascii=False, indent=2)

    return dpo_list
