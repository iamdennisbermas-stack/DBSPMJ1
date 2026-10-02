import os
import yaml

DATA_PATH = os.path.join(os.path.dirname(__file__), "main_category.yaml")

def get_main_categories(file_path=DATA_PATH):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return yaml.safe_load(f) or []