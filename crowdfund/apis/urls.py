from unicodedata import name
from django.urls import path, include
from .views import ListProjects, DetailProject

app_name = 'crowd_funding_apis'


urlpatterns = [
    path('list_projects/', ListProjects.as_view(),name='list_projects'),
    path('detail_project/<int:pk>/', DetailProject.as_view(),name='detail_project')
]
