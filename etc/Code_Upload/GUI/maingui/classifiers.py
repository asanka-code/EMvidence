from attr import attrs, attrib
import json
from sklearn.externals import joblib
from pathlib import Path
from typing import List, Dict
from sklearn.neural_network.multilayer_perceptron import MLPClassifier


@attrs
class FrequencyAnalaysis:
    freq = attrib(default=0)  # type: int
    sample_rate = attrib(default=0)  # type: int
    span = attrib(default=0)  # type: int

    def from_dict(self, input_dict: Dict):
        self.freq = int(input_dict["freq"])
        self.sample_rate = int(input_dict["sample_rate"])
        self.span = int(input_dict["span"])


@attrs
class Classifier:
    name = attrib(default="")  # type: str
    parts = attrib(default=[])  # type: List[str]
    frequency_analysis = attrib(default=[])  # type: List[FrequencyAnalaysis]
    location = attrib(default=None)  # type: Path

    @property
    def classifier(self):
        return joblib.load(self.location)

    def from_dict(self, input_dict: Dict):
        self.name = input_dict["name"]
        self.parts = input_dict["parts"]
        self.frequency_analysis = []
        for entry in input_dict["frequency_analysis"]:
            fa = FrequencyAnalaysis()
            fa.from_dict(entry)
            self.frequency_analysis.append(fa)
        self.location = Path(input_dict["location"])

    def from_str(self, input_str: str):
        self.from_dict(json.loads(input_str))

    def from_file(self, file_name):
        with open(file_name) as f:
            file_read = f.read()
            self.from_str(file_read)
