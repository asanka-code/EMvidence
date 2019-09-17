from django.contrib import admin

from .models import Signal, SignalTag, Annotation, Capture

admin.site.register(Signal)
admin.site.register(Annotation)
admin.site.register(Capture)
admin.site.register(SignalTag)