import os

def check_file_exists(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")

def ensure_dir_exists(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
