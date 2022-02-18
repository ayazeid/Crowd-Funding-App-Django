from django.urls import path
from . import views

urlpatterns = [
    path('', views.top_rated, name="home"),
    path('projectCategories', views.projectCategories, name="project_categories"),
    path('SearchTitle', views.SearchTitle, name="search_by_title"),
    path('SearchTag', views.SearchTag, name="search_by_tag"),
]