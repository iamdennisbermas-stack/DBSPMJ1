import json
import os
import smtplib
import urllib.request
import yaml
from email.mime.text import MIMEText

DATA_PATH = os.path.join(os.path.dirname(__file__), "pipeline.yaml")
PRECON_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../Stage2_CONSULT/PRECON/precon.yaml")
)

def send_pipeline_email(customer_name, customer_email, salesforce_email):
    body = f"""Dear {customer_name},

We are pleased to inform you that we have escalated your request for a pre-consultation process where one of our professional consultants will keep in touch with you.

Best regards,
Customer Relations Team
Knotica Solutions Inc.
Connecting Supply Chains. Integrated. Seamless. At Speed
"""
    msg = MIMEText(body)
    msg['Subject'] = "Pre-Consultation Request"
    msg['From'] = "info@knoticasolutions.com"
    msg['To'] = customer_email

    recipients = [customer_email]
    if salesforce_email:
        recipients.append(salesforce_email)

    smtp_password = os.getenv("SMTP_PASSWORD")
    if smtp_password:
        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.starttls()
            server.login("info@knoticasolutions.com", smtp_password)
            server.sendmail(msg['From'], recipients, msg.as_string())

    notify_webhook(f"Pipeline Escalated: Pre-consultation initiated for {customer_name} ({customer_email})")

def create_precon_entry(pipeline_record, precon_file=PRECON_PATH):
    records = []
    if os.path.exists(precon_file):
        with open(precon_file, "r") as f:
            records = yaml.safe_load(f) or []

    precon_record = {
        "Reference": f"PRE{pipeline_record.get('Reference', '000000')[3:]}",
        "LeadName": pipeline_record.get("CustomerName"),
        "LeadEmail": pipeline_record.get("CustomerEmail"),
        "SalesforceUser": pipeline_record.get("SalesforceEmail"),
        "StartDate": None,
        "EndDate": None,
        "SuspendDate": None,
        "MainCategory": None,
        "SubCategory": None,
        "Consultant": None,
        "Status": "NEW",
        "Notes": "Auto-generated from Sales Pipeline"
    }
    records.append(precon_record)
    
    os.makedirs(os.path.dirname(precon_file), exist_ok=True)
    with open(precon_file, "w") as f:
        yaml.safe_dump(records, f)

def notify_webhook(message):
    webhook_url = os.getenv("WEBHOOK_URL")
    if not webhook_url:
        return
    payload = json.dumps({"text": message}).encode("utf-8")
    req = urllib.request.Request(webhook_url, data=payload, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"Webhook notification failed: {e}")

if __name__ == "__main__":
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            pipeline_data = yaml.safe_load(f) or []
        for entry in pipeline_data:
            send_pipeline_email(entry["CustomerName"], entry["CustomerEmail"], entry.get("SalesforceEmail"))
            create_precon_entry(entry)