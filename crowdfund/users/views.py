from datetime import datetime, timezone

from django.http import HttpResponse
from django.shortcuts import render, redirect

from .tokens.token import TokenGenerator
from .forms import *

from django.shortcuts import render, redirect  
from django.contrib.auth import login, authenticate,logout
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  

from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  

# signals imports
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile

# Create your views here.
# - He can view his profile
def user_profile(request):
    context = {'user': Profile.objects.get(user=request.user)}
    return render(request, 'users/user_profile.html', context)


# - He can view his projects
# - He can view his donations

# - He can edit all his data except for the email, done
# - He can have extra optional info other than the info he added
# while registration (Birthdate, facebook profile, country), done
def update_profile(request):
    if request.method == 'POST':
        userform=EditUserForm(request.POST,instance=request.user)
        forminstance=UserProfileForm(request.POST, request.FILES,instance=Profile.objects.get(user=request.user))
        if userform.is_valid() and forminstance.is_valid():
            userform.save()
            updatedprofile=forminstance.save(commit=False)
            updatedprofile.user = request.user
            updatedprofile.save()
            return redirect('user_profile_page')
    else:
        userform = EditUserForm(instance=request.user)
        forminstance = UserProfileForm(instance=Profile.objects.get(user=request.user))
    context = {'form': forminstance,'userform':userform}
    return render(request, 'users/edit_user_profile.html', context)


# - User can delete his account (Note that there must be a
# confirmation message before deleting), done
def delete_profile(request):
    User.objects.get(username=request.user.username).delete()
    return HttpResponse('User deleted successfully')

  
def signup(request):  
    if request.method == 'POST':  
        form = SignupForm(request.POST)
        if form.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False  
            user.save() 
            Profile.objects.create(user=user)
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':TokenGenerator().make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Please confirm your email address to complete the registration')  
    else:  
        form = SignupForm()  
       
    return render(request, 'signup.html', {'form': form})  


def activate(request, uidb64, token):
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and TokenGenerator().check_token(user, token) and user.is_active == False: 
            print(user.date_joined)
            email_sent_at = user.date_joined
            now = datetime.now(timezone.utc)
            date_diffrince = (
               now-email_sent_at   
            ).seconds / 60
            print(date_diffrince)
            if date_diffrince < (24 * 60):
                user.is_active = True  
                user.save()
                return render(request,'confirmation.html')  
    else:  
        return HttpResponse('Activation link is invalid!')  
  
    
    
    
    
    
#///////////////////////////sign in /////////////////

def signin_user(request):
    context={}
    if request.method=="POST":
     try:
        myform=SigninForm(request.POST)
        u = User.objects.get(email=request.POST['email'])
        user = authenticate(username=u.username,password=request.POST['password'])
        if user is not None and user.is_active:
          login(request,user)     
          return redirect(user_profile)
        else:
            return HttpResponse('you should active your acount first... chick your Email')
     except:
         myform = SigninForm()
         context['form']=myform
         context['msg']='Wrong password or username ... '
         
         return render(request,'signin.html',context)
    else:
        myform = SigninForm()
        context['form']=myform
    return render(request,'signin.html',context)

#///////////////////////////logout /////////////////

def logout_user(request):
    request.session.clear()
    logout(request)
    return redirect('signin')
