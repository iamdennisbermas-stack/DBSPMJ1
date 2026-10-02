import os
import yaml
from PMJ.Stage1_SALES.SALES_PIPELINE import pipeline

def test_create_precon_entry(tmp_path):
    test_precon_file = os.path.join(tmp_path, "precon.yaml")
    pipeline_record = {
        "Reference": "SPI000001",
        "CustomerName": "Jane Smith",
        "CustomerEmail": "jane@prospect.com",
        "SalesforceEmail": "john@company.com"
    }
    pipeline.create_precon_entry(pipeline_record, precon_file=test_precon_file)
    
    assert os.path.exists(test_precon_file)
    with open(test_precon_file, "r") as f:
        data = yaml.safe_load(f)
    assert len(data) == 1
    assert data[0]["LeadName"] == "Jane Smith"
    assert data[0]["Reference"] == "PRE000001"