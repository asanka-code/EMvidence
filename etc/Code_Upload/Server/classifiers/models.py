import uuid  # Required for unique
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class ClassifierTag(models.Model):
    """Model representing a classifier record tag."""
    name = models.CharField(max_length=200, help_text='Enter a record tag (e.g. Education, Crime Scene, IoT)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Classifier(models.Model):
    owner = models.ForeignKey('auth.User', related_name='classifier', on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, help_text="Unique ID for Classifier for file storage")
    public = models.BooleanField(default=True)
    # Creation/Upload data is stored for listing etc
    timestamp = datetime.isoformat(datetime.utcnow()) + 'Z'
    created = models.DateTimeField(auto_now_add=True)
    # Tags allow the classifier to be classified
    tag = models.ManyToManyField(ClassifierTag, help_text='Select a tag for this record')

    name = models.CharField(max_length=200, help_text="Short description of the Classifier")
    description = models.TextField(help_text="Textual description of the Classifiers")

    ml = models.CharField(max_length=200, help_text="Machine Learning Toolkit used")
    score_labels = models.CharField(max_length=400, help_text="Semi-colon separated list of classifier score labels")
    data_preprocess = models.TextField(help_text="Optional Python code to pre-process inoput array")

    def __str__(self):
        """
        Easier representation of the Record for lists and admin
        :return: Classifier Record description
        """
        return self.name
