import requests
import os
import json
from sigmf.sigmffile import SigMFFile
from sigmf.sigmf_hash import calculate_sha512

# Current Directory and sample file
sample_datafile = "sample_recordings/example1.sigmf-data"
sample_metafile = "sample_recordings/example1.sigmf-meta"
file_sha = calculate_sha512(sample_datafile)

# Json
sample_capture1 = {'core:sample_start': 0}
sample_annotation1 = {'core:sample_count': 16, 'core:sample_start': 0}
sample_metadata = {"global": {"core:version": "0.0.1", 'core:datatype': 'f32', 'core:description': "Uploaded signal",
                              "core:sha512": file_sha},
                   "captures": [sample_capture1], "annotations": [sample_annotation1]}

# Save metadata to file
with open(sample_metafile, 'w+') as f:
    f.write(json.dumps(sample_metadata))

# Valdiate
signal1 = SigMFFile(metadata=sample_metadata, data_file=sample_datafile)
print(signal1)

print("Validation Passed") if signal1.validate() else print("Validation Failed")

# Upload
url_upload_json = "http://127.0.0.1:8000/signals-api/upload_json/"
url_upload_file = "http://127.0.0.1:8000/signals-api/upload_file/"
username = "Bob"
password = "Bob2019"

headers = {'Content-type': 'application/json'}

# Upload JSON
res = requests.post(url_upload_json, json=sample_metadata, auth=(username, password))
signal_uuid = 0  # Read back for Metadata upload post
if res.status_code == 200:
    signal_uuid = res.json()["uuid"]
    print(f"UUID: {signal_uuid}")

# Upload File
with open(sample_datafile, 'rb') as f:
    # headers = {'Content-type': 'multipart/form-data'}
    res = requests.post(url_upload_file, files={'file': f.read()},data={"signal_uuid": signal_uuid} , auth=(username, password))
    # print(res.json())
    print(res.status_code)
