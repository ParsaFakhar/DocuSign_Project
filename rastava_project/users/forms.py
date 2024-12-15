from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


# for register page
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}), max_length=50)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': ' '}), max_length=50)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ' '}), max_length=50)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ' '}), max_length=50)
    checker = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control form-check-input'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'checker']


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}), max_length=50)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': ' '}), max_length=50)

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']