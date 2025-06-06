import json
import re

def clean_value(val):
    if isinstance(val, str):
        return re.sub(r'[^\x00-\x7F]+', '', val)
    return val

def clean_dict(d):
    if isinstance(d, dict):
        return {k: clean_dict(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [clean_dict(i) for i in d]
    else:
        return clean_value(d)

with open('backup.json', 'r', encoding='utf-8', errors='ignore') as f:
    data = json.load(f)

cleaned_data = clean_dict(data)

with open('backup_clean.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

print('Arquivo backup_clean.json gerado sem caracteres especiais e JSON válido.')