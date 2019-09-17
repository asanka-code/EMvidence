import uuid # Required for unique
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

DATATYPES_CHOICES = sorted((item, item) for item in ["cf32", "numpy"])
LICENCES_CHOICES = sorted((item, item) for item in ["CC0", "Proprietary"])


class SignalSource(models.Model):
    signal_metadata = models.CharField(max_length=1000)


class SignalTag(models.Model):
    """Model representing a signal record tag."""
    name = models.CharField(max_length=200, help_text='Enter a record tag (e.g. Education, Crime Scene, IoT)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Signal(models.Model):
    """
    Signal is the base object representing a Signal Record, based on SigMF standard global namespace.
    """
    # Signal Records are owned by a particular investogator, defaulting to the uploader
    owner = models.ForeignKey('auth.User', related_name='signals', on_delete=models.CASCADE)
    # Each Signal Record has a Unique ID for storage purposes
    uuid = models.UUIDField(default=uuid.uuid4, help_text="Unique ID for Signal for file storage")
    # By default all Signal Records are public and viewable without being logged in
    public = models.BooleanField(default=True)
    # Creation/Upload data is stored for listing etc
    timestamp = datetime.isoformat(datetime.utcnow()) + 'Z'
    created = models.DateTimeField(auto_now_add=True)
    # Tags allow the signal to be classified
    tag = models.ManyToManyField(SignalTag, help_text='Select a tag for this record')

    # Global Strutcure from SigMF standard, adapted to default Django Models
    core_datatype = models.CharField(choices=DATATYPES_CHOICES, default="cf32", max_length=100,
                                     help_text="Required. Sample data format")
    core_offset = models.IntegerField(default=0, help_text="Index offset of the first sample. Defaults to 0")
    core_description = models.TextField(help_text="Textual description of the capture")
    core_author = models.TextField(default="Unknown", help_text="Name and optionally email address of the author")
    core_license = models.CharField(choices=LICENCES_CHOICES, default="CC0", max_length=100,
                                    help_text="Sample data license")
    core_date = models.CharField(max_length=100, help_text="Sample data license")  # Stored as text
    core_sha512 = models.TextField(help_text="SHA512 hash of the corresponding sample data file")
    core_version = models.TextField(default="0.0.1", help_text="Version of the SigMF specification")
    core_hw = models.TextField()

    def __str__(self):
        """
        Easier representaiton of the Record for lists and admin
        :return: Signal Record description
        """
        return self.core_description

    def get_captures(self):
        """
        Return all captures associated with the Signal Record
        :return: List of Capture objects
        """
        return Capture.objects.filter(signal=self)

    def num_captures(self):
        """
        Return number of Captures associated with the Signal Record
        :return: int
        """
        return len(self.get_captures())

    def get_annotations(self):
        """
        Return all annotations associated with the Signal Record
        :return: List of Annotation objects
        """
        return Annotation.objects.filter(signal=self)

    def num_annotations(self):
        """
        Return number of annotations associated with the Signal Record
        :return: int
        """
        return len(self.get_annotations())


class Capture(models.Model):
    signal = models.ForeignKey(Signal, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    # captures
    core_sample_start = models.IntegerField(default=0, help_text="Required. Index of first sample of this chunk")
    core_sampling_rate = models.FloatField(default=0, help_text="Sampling rate of signal (Sps)")
    core_frequency = models.FloatField(default=0, help_text="Center frequency of signal (Hz)")
    core_time = models.CharField(max_length=100, help_text="Start time of chunk, return as string")

    def __str__(self):
        return f"{self.signal.core_description}: Capture {self.core_sample_start}"

    class Meta:
        ordering = ("signal", "core_sample_start",)


class Annotation(models.Model):
    # Sorted by core:sample_start
    signal = models.ForeignKey(Signal, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    # annotations
    core_sample_start = models.IntegerField(help_text="Required. Index of first sample of this chunk")
    core_sample_count = models.IntegerField(help_text="Required. The number of samples described by this segment")
    core_comment = models.TextField(default="No Comment", help_text="Comment")

    def __str__(self):
        return f"{self.signal}: Annotation {self.core_sample_start} {self.core_comment}"

    class Meta:
        ordering = ("signal", "core_sample_start",)


