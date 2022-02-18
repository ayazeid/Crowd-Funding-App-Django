from django.urls import path
from .views import *

app_name='user_apis'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('<int:pk>/<str:token>', ActivateUser.as_view(), name='activate_user'),
    path('delete/', DeleteUser.as_view(), name='delete_user'),
    path('view', ViewProfile.as_view(), name='view_profile'),
    path('update/', UpdateProfile.as_view(), name='update_profile'),
]
