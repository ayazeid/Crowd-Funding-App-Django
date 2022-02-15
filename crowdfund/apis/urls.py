from django.urls import path
from .views import *

app_name = 'crowd_funding_apis'


urlpatterns = [
    path('list_projects/', ListProjects.as_view(),name='list_projects'),
    path('create_project/', CreateProject.as_view(),name='create_project'),
    path('view_project/<int:pk>/', ViewProject.as_view(),name='view_project'),
    path('delete_project/<int:pk>/', DeleteProject.as_view(),name='delete_project'),
    path('update_project/<int:pk>/', UpdateProject.as_view(),name='update_project'),
    path('donate_project/<int:id>/', DonateFund.as_view(),name='donate_project'),
    path('report_project/<int:id>/', ReportProject.as_view(),name='report_project'),
]
