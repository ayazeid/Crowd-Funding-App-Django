from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectList.as_view(), name='projects'),
    path('create-project/', views.ProjectCreate.as_view(), name='create-project'),
    # path('project/<title>', views.ProjectDetail.as_view())  # for DetailView
]
