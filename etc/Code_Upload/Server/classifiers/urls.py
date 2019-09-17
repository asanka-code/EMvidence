from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from classifiers import views

urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('classifiers/',
         views.IndexView.as_view(),
         name='index'),
    path('classifiers/<int:pk>/',
         views.DetailView.as_view(),
         name='detail'),
    path('classifiers-api/',
         views.ClassifiersList.as_view(),
         name='classifier-list'),
    path('classifiers-api/<int:pk>/',
         views.ClassifiersDetail.as_view(),
         name='classifier-detail'),
    path('classifiers-api/upload_json/',
         views.JSONUploadView.as_view(),
         name='jsonUpload'),
    path('classifiers-api/upload_file/',
         views.FileUploadView.as_view(),
         name='fileUpload'),
    path('classifiers-api/<int:pk>/',
         views.ClassifiersDetail.as_view(),
         name='classifiertag-detail'),


])
