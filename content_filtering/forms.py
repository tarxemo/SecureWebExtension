# users/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import *
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")



class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RestrictedURLForm(forms.ModelForm):
    class Meta:
        model = RestrictedURL
        fields = ['url']
        widgets = {
            'url': forms.URLInput(attrs={'class': 'border rounded p-2', 'placeholder': 'Enter the URL to restrict'}),
        }
        
from django import forms
from .models import RestrictedURL, RestrictedKeyword


class RestrictedKeywordForm(forms.ModelForm):
    class Meta:
        model = RestrictedKeyword
        fields = ['keyword']