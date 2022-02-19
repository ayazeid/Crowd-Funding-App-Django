from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User  


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

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email
        
        
class SigninForm(forms.ModelForm):
    password =  forms.CharField(max_length=32, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields =['email','password']