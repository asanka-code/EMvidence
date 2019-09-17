import sklearn
from classifiers import *

sample_classifier_dict = {
    "name": "simple-loop-2",
    "parts": ["ArduinoLeonardo"],
    "frequency_analysis": [{"freq": 18e6, "sample_rate": 20e6, "span": 10e6},
                           {"freq": 288e6, "sample_rate": 20e6, "span": 2e6}],
    "location": "maingui/classifiers/ie.ucd.compsci.project1.result1.clf"
}

sample_classifier_str = '{"name": "simple-loop-2", "parts": ["ArduinoLeonardo"], "frequency_analysis": [{"freq": 18000000.0, "sample_rate": 20000000.0, "span": 10000000.0}, {"freq": 288000000.0, "sample_rate": 20000000.0, "span": 2000000.0}], "location": "maingui/classifiers/ie.ucd.compsci.project1.result1.clf"}'


class BaseClassifierTest(object):
    """
    Base class for tests
    """

    def setup_method(self, method):
        self.test_classifier = Classifier()
        RuntimeError("Must be implemented")

    def teardown_method(self, method):
        pass

    def test_classifier_name(self):
        assert self.test_classifier.name == "simple-loop-2"

    def test_classifier_parts(self):
        assert self.test_classifier.parts == ["ArduinoLeonardo"]

    def test_classifier_frequency_analysis(self):
        assert self.test_classifier.frequency_analysis[0].freq == 18e6

    def test_classifier_location(self):
        assert self.test_classifier.location == Path("maingui/classifiers/ie.ucd.compsci.project1.result1.clf")

    def test_classifier_loading_classifier(self):
        assert type(self.test_classifier.classifier) == sklearn.neural_network.multilayer_perceptron.MLPClassifier


class TestClassifiersDict(BaseClassifierTest):

    def setup_method(self, method):
        """
        Create classifier used for testing, using dictionary as source
        :param method: test to be run
        :return:
        """
        self.test_classifier = Classifier()
        self.test_classifier.from_dict(sample_classifier_dict)


class TestClassifiersStr(BaseClassifierTest):

    def setup_method(self, method):
        """
        Create classifier used for testing, using string as source
        :param method: test to be run
        :return:
        """
        self.test_classifier = Classifier()
        self.test_classifier.from_str(sample_classifier_str)
