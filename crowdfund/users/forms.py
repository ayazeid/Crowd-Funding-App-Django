from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User  

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('email',)

  
class SignupForm(UserCreationForm):  
    email = forms.EmailField(max_length=200, help_text='Required')  
    class Meta:  
        model = User  
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']
        
        
class SigninForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields =['email','password']