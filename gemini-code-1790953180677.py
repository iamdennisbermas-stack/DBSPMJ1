import os
import yaml

DATA_PATH = os.path.join(os.path.dirname(__file__), "sub_category.yaml")

def get_subcategories(main_code, file_path=DATA_PATH):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        subs = yaml.safe_load(f) or []
    return [s for s in subs if s.get('MainCode') == main_code]

def validate_subcategory(main_code, sub_code, file_path=DATA_PATH):
    subs = get_subcategories(main_code, file_path)
    return any(s.get('CODE') == sub_code for s in subs)