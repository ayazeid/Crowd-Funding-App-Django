from django.http import HttpResponse
from django.shortcuts import render, redirect

from .tokens.token import TokenGenerator
from .models import *
from .forms import *

from django.shortcuts import render, redirect  
from django.contrib.auth import login, authenticate,logout
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
 
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  

# Create your views here.
def signup(request):
    pass
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

  
def signup(request):  
    if request.method == 'POST':  
        form = SignupForm(request.POST)  
        if form.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False  
            
            user.save()  
           
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
    if user is not None and TokenGenerator().check_token(user, token):  
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
        #   print (request.user.email)
          return render(request,'home.html')      
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
