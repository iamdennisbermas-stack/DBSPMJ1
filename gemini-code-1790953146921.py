import os
import yaml
from PMJ.Stage2_CONSULT.PRECON import precon

def test_update_precon_status(tmp_path):
    test_file = os.path.join(tmp_path, "precon.yaml")
    record = {
        "Reference": "PRE000001",
        "LeadName": "Jane Smith",
        "LeadEmail": "jane@prospect.com",
        "Status": "NEW"
    }
    precon.update_precon_status(record, "Submitted", file_path=test_file)
    
    with open(test_file, "r") as f:
        records = yaml.safe_load(f)
    assert records[0]["Status"] == "Submitted"
    
    trigger_file = os.path.join(tmp_path, "precon_trigger_submitted.yaml")
    assert os.path.exists(trigger_file)