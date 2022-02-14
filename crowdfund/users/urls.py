from django.urls import path
from .views import *

urlpatterns = [
    path('<str:username>', user_profile, name='user_profile_page'),
    path('edit/<str:username>', update_profile, name='edit_profile_page'),
    path('delete/<str:username>', delete_profile, name='delete_user_profile')
]
