from datetime import datetime
import os
import json
import django
from signals.models import Signal, Capture, Annotation
from signals.serializers import SignalSerializer, UserSerializer
from signals.permissions import IsOwnerOrReadOnly
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
        'users': reverse('user-list', request=request, format=format),
        'signals': reverse('signal-list', request=request, format=format)
    })


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class IndexView(generic.ListView):
    template_name = 'signals/index.html'
    context_object_name = 'latest_signal_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Signal.objects.filter(
            created__lte=timezone.now()
        ).order_by('-created')[:5]


class DetailView(generic.DetailView):
    model = Signal
    template_name = 'signals/detail.html'


class SignalsList(generics.ListCreateAPIView):
    queryset = Signal.objects.all()
    serializer_class = SignalSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SignalsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Signal.objects.all()
    serializer_class = SignalSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class JSONUploadView(APIView):
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        signmf = SigMFFile(metadata=request.data)
        if signmf.validate():
            sig = Signal(owner=User.objects.get(username=request.user.username))
            j = request.data

            # Globals
            if "core:datatype" in j["global"]:
                sig.core_datatype = j["global"]["core:datatype"]
            if "core:offset" in j["global"]:
                sig.core_offset = j["global"]["core:offset"]
            if "core:description" in j["global"]:
                sig.core_description = j["global"]["core:description"]
            else:
                timestamp = datetime.isoformat(datetime.utcnow()) + 'Z'
                sig.core_description = f"{request.user.username}: {timestamp}"
            if "core:author" in j["global"]:
                sig.core_author = j["global"]["core:author"]
            else:
                sig.core_author = request.user.username
            if "core:license" in j["global"]:
                sig.core_license = j["global"]["core:license"]
            if "core:date" in j["global"]:
                sig.core_date = j["global"]["core:date"]
            if "core:sha512" in j["global"]:
                sig.core_sha512 = j["global"]["core:sha512"]
            if "core:version" in j["global"]:
                sig.core_version = j["global"]["core:version"]
            if "core:hw" in j["global"]:
                sig.core_hw = j["global"]["core:hw"]

            sig.save()

            # Captures
            for jcapture in j["captures"]:
                c = Capture()
                c.signal = sig
                c.core_sample_start = jcapture["core:sample_start"]
                if "core:frequency" in jcapture:
                    c.core_frequency = jcapture["core:frequency"]
                if "core:sampling_rate" in jcapture:
                    c.core_sampling_rate = jcapture["core:sampling_rate"]
                if "core:time" in jcapture:
                    c.core_time = jcapture["core:time"]
                c.save()
            # Annotations
            for jannotation in j["annotations"]:
                a = Annotation()
                a.signal = sig
                a.core_sample_start = jannotation["core:sample_start"]
                a.core_sample_count = jannotation["core:sample_count"]
                if "core:comment" in jannotation:
                    a.core_comment = jannotation["core:comment"]
                a.save()
            responseData = {"uuid": f"{sig.uuid}"}
            return JsonResponse(responseData)
        else:
            return Response(status=111)


class FileUploadView(APIView):
    """
    Upload a file. A signal_uuid must be provided.
    The UUID of the signal record must match a user owned signal.
    """
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):

        # Get user and file
        if request.user.username:
            user = User.objects.get(username=request.user.username)
            signal = None
            up_file = request.FILES['file']
            signal_id = request.POST['signal_uuid']
            # Try to find the related Signal. Return Not Found if no signal matched
            try:
                signal = get_object_or_404(Signal, uuid=signal_id)
                # Return 401 of the Signal is not owned by the logged in user.
                if signal.owner != user:
                    return Response(status=401)
            except django.core.exceptions.ValidationError:
                return Response(status=404)

            # Upload the file, replacing an existing one
            upload_dir = f"/tmp/uploads/signals"
            if not os.path.exists(upload_dir):
                os.mkdir(upload_dir)
            upload_filename = f"{upload_dir}/{signal_id}"
            if os.path.exists(upload_filename):
                os.remove(upload_filename)

            destination = open(upload_filename, 'wb+')
            for chunk in up_file.chunks():
                destination.write(chunk)
            destination.close()

            # Check the SHA512
            uploaded_sha = calculate_sha512(upload_filename)
            if signal.core_sha512 != uploaded_sha:
                return Response(status=409)

            return Response(status=200)
            # return JsonResponse(f"{signal_id}: {upload_filename}", status=204)

        else:
            return Response(status=401)
