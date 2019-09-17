from django.contrib import admin

from .models import Classifier, ClassifierTag

admin.site.register(Classifier)
admin.site.register(ClassifierTag)
