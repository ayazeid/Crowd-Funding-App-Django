from django.shortcuts import render
from .models import *


# Create your views here.
# - He can view his profile
def user_profile(request, username):
    context = {'user': Profile.objects.get(username=username)}
    return render(request, 'users/user_profile.html', context)


# - He can view his projects
# - He can view his donations

# - He can edit all his data except for the email
# - He can have extra optional info other than the info he added
# while registration (Birthdate, facebook profile, country)
def update_profile(request):
    pass


# - User can delete his account (Note that there must be a
# confirmation message before deleting)
def delete_profile(request):
    pass
