import re

def remove_special_characters(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

# Tentar abrir com latin1
with open('backup.json', 'r', encoding='latin1') as f:
    data = f.read()

data_clean = remove_special_characters(data)

with open('backup_clean.json', 'w', encoding='utf-8') as f:
    f.write(data_clean)

print('Arquivo backup_clean.json gerado sem caracteres especiais.')