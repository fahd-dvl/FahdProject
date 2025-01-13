from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

class SignupForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets={
            'username': forms.TextInput(),
            'email': forms.EmailInput(),
            'password': forms.PasswordInput()
        }

    def clean(self):
       cleaned_data= super().clean()
       password = cleaned_data.get('password')
       confirm_password = cleaned_data.get('confirm_password')
       if password != confirm_password:
           raise forms.ValidationError("Password do not match")
       return cleaned_data
    

           