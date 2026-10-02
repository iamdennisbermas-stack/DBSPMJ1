import json
import os
import smtplib
import sys
import urllib.request
import yaml
from email.mime.text import MIMEText

DATA_PATH = os.path.join(os.path.dirname(__file__), "precon.yaml")

def update_precon_status(precon_record, new_status, file_path=DATA_PATH):
    precon_record['Status'] = new_status
    records = []
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            records = yaml.safe_load(f) or []
    
    updated = False
    for i, r in enumerate(records):
        if r.get("Reference") == precon_record.get("Reference"):
            records[i] = precon_record
            updated = True
            break
    if not updated:
        records.append(precon_record)

    with open(file_path, "w") as f:
        yaml.safe_dump(records, f)

    trigger_file = os.path.join(os.path.dirname(file_path), f"precon_trigger_{new_status.lower()}.yaml")
    with open(trigger_file, "w") as f:
        yaml.safe_dump(precon_record, f)

def send_precon_email(precon_record, status):
    templates = {
        "Submitted": (
            "Follow-Up: Discovery Call Notes & Next Steps",
            f"Dear {precon_record.get('LeadName')},\n\nThank you for taking the time to speak with us during the discovery call. We look forward to collaborating on the next phase.\n\nBest regards,\nKnotica Solutions Inc.\nConnecting Supply Chains. Integrated. Seamless. At Speed"
        ),
        "Suspended": (
            "Consultation Suspended",
            f"Dear {precon_record.get('LeadName')},\n\nYour consultation process has been temporarily suspended. Our team will reach out once it is ready to resume.\n\nBest regards,\nKnotica Solutions Inc."
        ),
        "Cancelled": (
            "Consultation Cancelled",
            f"Dear {precon_record.get('LeadName')},\n\nWe regret to inform you that your consultation process has been cancelled. Please contact us if you wish to re-initiate.\n\nBest regards,\nKnotica Solutions Inc."
        ),
        "Resumed": (
            "Consultation Resumed",
            f"Dear {precon_record.get('LeadName')},\n\nWe are pleased to inform you that your consultation process has now resumed. Our consultant will be in touch shortly.\n\nBest regards,\nKnotica Solutions Inc."
        )
    }

    if status not in templates:
        return

    subject, body = templates[status]
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "info@knoticasolutions.com"
    msg['To'] = precon_record['LeadEmail']

    recipients = [precon_record['LeadEmail']]
    if precon_record.get("ConsultantEmail"):
        recipients.append(precon_record["ConsultantEmail"])

    smtp_password = os.getenv("SMTP_PASSWORD")
    if smtp_password:
        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.starttls()
            server.login("info@knoticasolutions.com", smtp_password)
            server.sendmail(msg['From'], recipients, msg.as_string())

    notify_webhook(f"PRECON Notification Sent [{status}]: {precon_record.get('Reference')} - {precon_record.get('LeadName')}")

def notify_webhook(message):
    webhook_url = os.getenv("WEBHOOK_URL")
    if not webhook_url:
        return
    payload = json.dumps({"text": message}).encode("utf-8")
    req = urllib.request.Request(webhook_url, data=payload, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"Webhook error: {e}")

def handle_status(precon_record):
    status = precon_record.get("Status")
    send_precon_email(precon_record, status)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        trigger_file = sys.argv[1]
        if os.path.exists(trigger_file):
            with open(trigger_file, "r") as f:
                record = yaml.safe_load(f)
            if record:
                handle_status(record)