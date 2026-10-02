import os
from PMJ.Stage1_SALES.SALESFORCE import salesforce

def test_add_and_list_salesforce(tmp_path):
    test_file = os.path.join(tmp_path, "salesforce.yaml")
    record = {"Name": "Test User", "Email": "test@company.com", "Status": "Active"}
    salesforce.add_salesforce_record(record, file_path=test_file)
    records = salesforce.list_salesforce_records(file_path=test_file)
    assert len(records) == 1
    assert records[0]["Name"] == "Test User"