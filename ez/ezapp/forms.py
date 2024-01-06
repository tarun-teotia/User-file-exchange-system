from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Record

choice = [
    ('1', 'ops'),
    ('2', 'client')
]

# Create formsclass
class SignUpForm(UserCreationForm):
    Name=forms.CharField(label='Name',widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.EmailField(label='Email Address',widget=forms.TextInput(attrs={'class':'form-control'}))
    username=forms.CharField(label='Username',widget=forms.TextInput(attrs={'class':'form-control'}))
    user_type=forms.ChoiceField(label='Ops/Client', widget=forms.RadioSelect,choices=choice)
    password1=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Password Confirm',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model=User
        fields=('Name','email','username','user_type','password1','password2')

# create form to add customer data 
class addrecord(forms.ModelForm):
    file=forms.FileField(label='Upload')
    class Meta:
        model=Record
        fields=('file',)

