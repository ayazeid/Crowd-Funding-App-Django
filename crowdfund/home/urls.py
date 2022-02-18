from django.urls import path
from . import views

urlpatterns = [
    path('', views.top_rated, name="home"),
    path('projectCategories', views.projectCategories, name="project_categories"),
]