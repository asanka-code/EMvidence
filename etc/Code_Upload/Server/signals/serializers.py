from rest_framework import serializers
from signals.models import Signal, DATATYPES_CHOICES, LICENCES_CHOICES
from django.contrib.auth.models import User


class SignalSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Signal
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    signals = serializers.HyperlinkedRelatedField(many=True, view_name='signal-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'signals')
