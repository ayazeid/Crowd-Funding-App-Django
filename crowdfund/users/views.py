from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .forms import *


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
def update_profile(request, username):
    if request.method == 'POST':
        UserProfileForm(request.POST, instance=Profile.objects.get(username=username)).save()
        return redirect('user_profile_page', username)
    else:
        forminstance = UserProfileForm(instance=Profile.objects.get(username=username))
        context = {'form': forminstance, 'user': username}
        return render(request, 'users/edit_user_profile.html', context)


# - User can delete his account (Note that there must be a
# confirmation message before deleting)
def delete_profile(request,username):
    Profile.objects.filter(username=username).delete()
    # return redirect('')
    return HttpResponse('User deleted successfully')

