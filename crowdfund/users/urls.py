from django.urls import path
from .views import *

urlpatterns = [
    path('<str:username>', user_profile, name='user_profile_page'),
]
