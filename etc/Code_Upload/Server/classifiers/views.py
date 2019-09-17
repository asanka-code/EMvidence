from datetime import datetime
import os
import json
import django
from classifiers.models import Classifier, ClassifierTag
from classifiers.serializers import ClassifierSerializer, FileUploadSerializer
from classifiers.permissions import IsOwnerOrReadOnly
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.views import APIView
from sigmf.sigmffile import SigMFFile
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from sigmf.sigmf_hash import calculate_sha512
from rest_framework.response import Response
from django.http import JsonResponse

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'classifiers': reverse('classifier-list', request=request, format=format)
    })


class IndexView(generic.ListView):
    template_name = 'classifiers/index.html'
    context_object_name = 'latest_classifier_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Classifier.objects.filter(
            created__lte=timezone.now()
        ).order_by('-created')[:5]


class DetailView(generic.DetailView):
    model = Classifier
    template_name = 'classifiers/detail.html'


class ClassifiersList(generics.ListCreateAPIView):
    queryset = Classifier.objects.all()
    serializer_class = ClassifierSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ClassifiersDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Classifier.objects.all()
    serializer_class = ClassifierSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class JSONUploadView(APIView):
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        classifier = Classifier(owner=User.objects.get(username=request.user.username))
        j = request.data

        # Globals
        classifier.name = j["name"]
        classifier.description = j["description"]
        classifier.ml = j["ml"]
        classifier.score_labels = j["score_labels"]
        classifier.data_preprocess = j["data_preprocess"]

        classifier.save()
        tags_all = [c.name for c in ClassifierTag.objects.all()]
        print(tags_all)
        for tags in j["tags"]:
            if tags not in tags_all:
                c = ClassifierTag()
                c.classifier = classifier
                c.name = tags
                c.save()

        responseData = {"uuid": f"{classifier.uuid}"}
        return JsonResponse(responseData)





class FileUploadView(APIView):
    """
    Upload a file. A classifier_uuid must be provided.
    The UUID of the signal record must match a user owned signal.
    """
    parser_classes = (MultiPartParser,)

    serializer_class = FileUploadSerializer
    def post(self, request, format=None):

        # Get user and file
        if request.user.username:
            user = User.objects.get(username=request.user.username)
            classifier = None
            up_file = request.FILES['file']
            classifier_id = request.POST['classifier_uuid']
            # Try to find the related Signal. Return Not Found if no signal matched
            try:
                classifier = get_object_or_404(Classifier, uuid=classifier_id)
                # Return 401 of the Classifier is not owned by the logged in user.
                if classifier.owner != user:
                    return Response(status=401)
            except django.core.exceptions.ValidationError:
                return Response(status=404)

            # Upload the file, replacing an existing one
            upload_dir = f"/tmp/uploads/classifiers/"
            if not os.path.exists(upload_dir):
                os.mkdir(upload_dir)
            upload_filename = f"{upload_dir}/{classifier_id}"
            if os.path.exists(upload_filename):
                os.remove(upload_filename)

            destination = open(upload_filename, 'wb+')
            for chunk in up_file.chunks():
                destination.write(chunk)
            destination.close()

            return Response(status=200)


        else:
            return Response(status=401)
