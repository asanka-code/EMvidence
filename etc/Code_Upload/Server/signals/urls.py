from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from signals import views

urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('signals/',
         views.IndexView.as_view(),
         name='index'),
    path('signals/<int:pk>/',
         views.DetailView.as_view(),
         name='detail'),
    path('signals-api/',
         views.SignalsList.as_view(),
         name='signal-list'),
    path('signals-api/<int:pk>/',
         views.SignalsDetail.as_view(),
         name='signal-detail'),
    path('signals-api/upload_json/',
         views.JSONUploadView.as_view(),
         name='jsonUpload'),
    path('signals-api/upload_file/',
         views.FileUploadView.as_view(),
         name='fileUpload'),
    path('signals-api/<int:pk>/',
         views.SignalsDetail.as_view(),
         name='signaltag-detail'),
    path('users/',
         views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/',
         views.UserDetail.as_view(), name='user-detail'),

])
