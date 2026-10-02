import os
import yaml

DATA_PATH = os.path.join(os.path.dirname(__file__), "lead.yaml")

def add_lead_record(record, file_path=DATA_PATH):
    records = list_lead_records(file_path) or []
    records.append(record)
    with open(file_path, "w") as f:
        yaml.safe_dump(records, f)

def list_lead_records(file_path=DATA_PATH):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return yaml.safe_load(f) or []