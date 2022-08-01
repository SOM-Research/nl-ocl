import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent

def read_file(path):
    file = open(path, "r")
    data = file.read()
    file.close()
    return data
def wikisql_json_path():
    return os.path.join(BASE_DIR, 'data', 'dev.jsonl')
def wikisql_json_tables_path():
    return os.path.join(BASE_DIR, 'data', 'dev.tables.jsonl')
def spider_json_path():
    return os.path.join(BASE_DIR, 'data', 'spider', 'dev.json')
def spider_json_tables_path():
    return os.path.join(BASE_DIR, 'data', 'spider', 'tables.json')    