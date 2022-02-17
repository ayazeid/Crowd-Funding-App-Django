from django.urls import path
from .views import *

urlpatterns = [
    # path('<str:username>', user_profile, name='user_profile_page'),
    path('profile', user_profile, name='user_profile_page'),
    path('edit', update_profile, name='edit_profile_page'),
    path('delete', delete_profile, name='delete_user_profile')
]
