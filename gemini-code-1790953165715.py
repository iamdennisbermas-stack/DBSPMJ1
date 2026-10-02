import os
from PMJ.Stage1_SALES.LEAD import lead

def test_add_and_list_lead(tmp_path):
    test_file = os.path.join(tmp_path, "lead.yaml")
    record = {"Name": "Jane Lead", "Email": "jane@lead.com", "Status": "Active"}
    lead.add_lead_record(record, file_path=test_file)
    records = lead.list_lead_records(file_path=test_file)
    assert len(records) == 1
    assert records[0]["Name"] == "Jane Lead"