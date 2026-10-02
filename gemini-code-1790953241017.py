import os
import yaml

DATA_PATH = os.path.join(os.path.dirname(__file__), "templates.yaml")

def load_templates(file_path=DATA_PATH):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r") as f:
        return yaml.safe_load(f) or {}

def format_pitch(template_id, customer_data, file_path=DATA_PATH):
    data = load_templates(file_path)
    templates = data.get("templates", [])
    for t in templates:
        if t["id"] == template_id:
            subject = t["subject"].format(**customer_data)
            body = t["body"].format(**customer_data)
            return {"subject": subject, "body": body}
    raise ValueError(f"Template {template_id} not found.")