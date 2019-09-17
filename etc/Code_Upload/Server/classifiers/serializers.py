from rest_framework import serializers
from classifiers.models import Classifier
from django.contrib.auth.models import User


class ClassifierSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Classifier
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    classifiers = serializers.HyperlinkedRelatedField(many=True, view_name='classifier-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'classifiers')


class FileUploadSerializer(serializers.Serializer):
    limit = serializers.CharField(max_length=200, help_text='classifier uuid', required=True)
