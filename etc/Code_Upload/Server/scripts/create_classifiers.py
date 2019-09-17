import requests


json1 = {"name": "ECC Detection (Arduino)",
         "description": "Binary Classifier to detect if device is performing Elliptic-curve cryptography on the Arduino Leonardo",
         "ml": "Keras",
         "score_labels": 'Not ECC;ECC Detected',
         "data_preprocess": "\n\
def shape_input(input_array, number_windows=46, window_length=100):\n\
    output_array = [0] * number_windows\n\
    for i in range(number_windows):\n\
        idx = (i * window_length)\n\
        output_array[i] = input_array[idx:(idx + window_length)]\n\
    return output_array",
         "tags": ["Keras", "ECC", "Arduino", "Cryptography"]}
json2 = {"name": "ECC Detection (Arduino) v2",
         "description": "Binary Classifier to detect if device is performing Elliptic-curve cryptography on the Arduino Leonardo",
         "ml": "Keras",
         "data_preprocess": '',
         "score_labels": 'Not ECC;ECC Detected',
         "tags": ["Keras", "ECC", "Arduino", "Cryptography"]}
json3 = {"name": "Loop Detection (Arduino)",
         "description": "Binary Classifier to determine if the Arduino is Idle",
         "ml": "Scikit",
         "data_preprocess": '',
         "score_labels": 'Not Idle;Idle',
         "tags": ["Scikit", "Arduino", "Arduino"]}


data1 = "sample_classifiers/lstm-ecc-detector-trace-length-100-window-size-10-step-size-2.h5"
data2 = "sample_classifiers/lstm-ecc-detector-trace-length-100-window-size-10-step-size-2_version2.h5"
data3 = "sample_classifiers/loop2_classifier.clf"

# Upload
url_upload_json = "http://127.0.0.1:8000/classifiers-api/upload_json/"
url_upload_file = "http://127.0.0.1:8000/classifiers-api/upload_file/"
username = "Bob"
password = "Bob2019"

headers = {'Content-type': 'application/json'}

sample_classifiers = [{"json": json1, "data": data1},
                      {"json": json2, "data": data2},
                      {"json": json3, "data": data3}]

for sample in sample_classifiers:
    sample_metadata = sample['json']
    sample_datafile = sample['data']

    # Upload JSON
    res = requests.post(url_upload_json, json=sample_metadata, auth=(username, password))
    classifier_uuid = 0  # Read back for Metadata upload post
    if res.status_code == 200:
        classifier_uuid = res.json()["uuid"]
        print(f"UUID: {classifier_uuid}")

    # Upload File
    with open(sample_datafile, 'rb') as f:
        res = requests.post(url_upload_file, files={'file': f.read()}, data={"classifier_uuid": classifier_uuid} , auth=(username, password))
        print(res.status_code)
