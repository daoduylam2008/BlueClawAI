import json

data = []
file_path = 'valid.jsonl'

with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            json_object = json.loads(line.strip())
            data.append(json_object)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON on line: {e}")

# 'data' is now a list of Python dictionaries
for item in data:
    print(item)