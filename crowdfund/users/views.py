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

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from projects.models import Project,UserDonation,ProjectReport,ReportComment,Comment,Rating
from django.db.models import Sum






# Create your views here.
# profile view
def user_profile(request):
 if (request.user.is_authenticated):
    # - He can view his profile
    loged_user = Profile.objects.get(user=request.user)
    # - He can view his projects
    user_projects = Project.objects.filter(project_owner=request.user)
    # - He can view his donations
    user_donations= UserDonation.objects.filter(user_donated=request.user)
    total_donations_amount = sum([donation.amount for donation in UserDonation.objects.filter(user_donated=request.user) ])
    reported_projects = ProjectReport.objects.all()
    reported_comments = ReportComment.objects.all()
    total_ratings = Rating.objects.all()
    #raters_count = Rating.objects.filter(project_id=self.kwargs["pk"]).count()
    total_donations_project = UserDonation.objects.all()
    context = {'user': loged_user,'projects':user_projects,'donations':user_donations,'total_donations':total_donations_amount,'reported_projects':reported_projects,'reported_comments':reported_comments,'total_ratings':total_ratings,'total_donations_project':total_donations_project}
    return render(request, 'users/user_profile.html', context)
 else:
     return redirect('signin')




# edit profile view
def update_profile(request):
 if (request.user.is_authenticated):
    if request.method == 'POST':
        # - He can edit all his data except for the email, done
        # - He can have extra optional info other than the info he added
        # while registration (Birthdate, facebook profile, country), done
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
 else:
     return redirect('signin')


def delete_profile(request):
 if (request.user.is_authenticated):
    # - User can delete his account (Note that there must be a
    # confirmation message before deleting), done
    User.objects.get(username=request.user.username).delete()
    return HttpResponse('User deleted successfully')
 else:
     return redirect('signin')
  
def signup(request):  
    if request.method == 'POST':  
        form = SignupForm(request.POST)
        profile = UserProfileForm(request.POST,request.FILES)
        if form.is_valid() and profile.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False  
            user.save() 
            uprofile=profile.save(commit=False)
            uprofile.user=user
            uprofile.save()
           
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
        profile= UserProfileForm()
    return render(request, 'signup.html', {'form': form,'profile':profile})  


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
        elif not user.is_active:
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
