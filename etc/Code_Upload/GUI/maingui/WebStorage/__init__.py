import json
import requests
from typing import Optional
from tempfile import mkstemp


class WebStorage:

    def __init__(self, base_url: str):
        """
        Initliase WebStorage
        :param base_url: Base URL
        """
        self._url = base_url
        self._username = None
        self._password = None

    def login_details(self, username: str, password: str):
        """
        Save login details
        :param username:
        :param password:
        :return:
        """
        self._username = username
        self._password = password

    def get_idn_db(self) -> (bool, dict):
        pass

    def get_idb_images(self) -> (bool, dict):
        pass

    def get_json_api(self, api_name) -> (bool, dict):
        """
        Query the WEb backend API using the login details, returns a JSON object
        :param api_name: namespace for API, e.g. signals
        :return: success, dictionary
        """
        url = f"{self._url}/{api_name}-api/"
        try:
            res = requests.get(url, auth=(self._username, self._password))
        except:
            return False, None
        if res.status_code == 200:
            res_json = res.json()
            return True, res_json
        else:
            return False, None

    def get_classifiers(self) -> (bool, dict):
        return self.get_json_api("classifiers")

    def get_signals(self) -> (bool, dict):
        return self.get_json_api("signals")

    def download_file(self, namespace: str, uuid: str) -> Optional[str]:
        """
        Download the classifier specified by the supplied UUID and return it's location
        :param namespace: Namespace to download file from, e.g. signals
        :param uuid: The UUID of the classifier to download
        :return: A temp file on the local hard disk, or None if it fails
        """

        url = f"{self._url}/static/{namespace}/{uuid}"

        _, local_filename = mkstemp()
        r = requests.get(url, auth=(self._username, self._password))
        if r.status_code == 200:
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=512 * 1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
            return local_filename
        else:
            return None

    def download_classifier(self, uuid: str) -> Optional[str]:
        return self.download_file("classifiers", uuid)

    def download_signal(self, uuid: str) -> Optional[str]:
        """
        Download a Signal Record to a temporary file
        :param uuid: The UUID of the record
        :return: The file path if successful
        """
        return self.download_file("signals", uuid)

    def upload_signal(self, metadata: dict, datafile: str) -> Optional[str]:
        """
        Upload a Signal Record, return the UUID if successfully
        :param metadata: JSON dict of the SigMF data descriving the record
        :param datafile: Path to the data file to upload
        :return:
        """
        # Upload
        url_upload_json = f"{self._url}/signals-api/upload_json/"
        url_upload_file = f"{self._url}/signals-api/upload_file/"

        # Upload JSON
        res = requests.post(url_upload_json, json=metadata, auth=(self._username, self._password))
        if res.status_code == 200:
            signal_uuid = res.json()["uuid"]
        else:
            return None

        # Upload File
        with open(datafile, 'rb') as f:
            # headers = {'Content-type': 'multipart/form-data'}
            res = requests.post(url_upload_file, files={'file': f.read()}, data={"signal_uuid": signal_uuid},
                                auth=(self._username, self._password))
            if res.status_code == 200:
                return signal_uuid
            else:
                return None

    def upload_classifier(self, metadata: dict, datafile: str) -> Optional[str]:
        """
        Upload a Classifier_uuid return the UUID if successfully
        :param metadata: JSON dict containing the classifier details, e.g. name, type and tags
        :param datafile: Path to the data file to upload, e.g. h5 file
        :return:
        """
        # Upload
        url_upload_json = f"{self._url}/classifiers-api/upload_json/"
        url_upload_file = f"{self._url}/classifiers-api/upload_file/"

        # Upload JSON
        res = requests.post(url_upload_json, json=metadata, auth=(self._username, self._password))
        if res.status_code == 200:
            classifier_uuid = res.json()["uuid"]
        else:
            return None

        # Upload File
        with open(datafile, 'rb') as f:
            # headers = {'Content-type': 'multipart/form-data'}
            res = requests.post(url_upload_file, files={'file': f.read()}, data={"classifier_uuid": classifier_uuid},
                                auth=(self._username, self._password))
            if res.status_code == 200:
                return classifier_uuid
            else:
                return None


if __name__ == "__main__":
    web = WebStorage("http://127.0.0.1:8000")
    web.login_details("Bob", "Bob2019")

    err, signals = web.get_signals()
    # print(signals)
    for sig in signals:
        print(f"{sig['core_description']}|{sig['owner']}|{sig['created']}")

    err, classifiers = web.get_classifiers()
    # print(classifiers)
    for sig in classifiers:
        print(f"{sig['name']}|{sig['owner']}|{sig['uuid']}")

    uuid0 = classifiers[0]['uuid']
    print(uuid0)
    fout = web.download_classifier(uuid0)
    print(fout)
