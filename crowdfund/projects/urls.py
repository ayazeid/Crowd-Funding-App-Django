from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectList.as_view(), name='projects'),
    path('create-project/', views.ProjectCreate.as_view(), name='create-project'),
    path('project/<int:pk>', views.ProjectDetail.as_view(), name='details-project'),
    path('create-comment/<int:pk>', views.CommentCreate.as_view(), name='create-comment'),
    path('donate-project/<int:pk>', views.DonateCreate.as_view(), name='donate-project'),
    path('rate-project/<int:pk>', views.RateCreate.as_view(), name='rate-project'),
    path('delete-project/<int:pk>', views.projectDelete, name='delete-project'),
]
