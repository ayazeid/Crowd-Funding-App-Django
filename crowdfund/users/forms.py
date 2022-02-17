from dataclasses import field
import profile
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User  
# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _

# egyptian phone number validation
# def validate_egyptian_number(value):
#     if not any(re.match(pattern, value) for pattern in [r"011+[0-9]{8}", r"012+[0-9]{8}", r"015+[0-9]{8}",""]):
#         raise ValidationError(
#             _('%(value)s is not a valid egyptian number'),
#             params={'value': value},
#         )



# class ProfileCreateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['first_name','last_name','username','email']

# class ExtraFields(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['user','phone','profile_picture']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone','profile_picture','birth_date','facebook_profile','country']

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username']
        

#################################################
class SignupForm(UserCreationForm):  
    email = forms.EmailField(max_length=200, help_text='Required')  
    class Meta:  
        model = User  
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']
        
        
class SigninForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields =['email','password']