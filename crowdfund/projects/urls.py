from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectList.as_view(), name='projects'),
]
