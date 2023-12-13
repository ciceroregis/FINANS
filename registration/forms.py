from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nome completo",
                "class": "form-control",
                "id": "first_name"
            }
        ))

    username = forms.CharField(

        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control",
                "id": "username"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control",
                "id": "email"

            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Senha",
                "class": "form-control",
                "id": "password1"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Senha de verificação",
                "class": "form-control",
                "id": "password2"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'password1', 'password2')


class UserChangeData(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nome completo",
                "class": "form-control",
                "id": "first_name"
            }
        ))

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control",
                "id": "username"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control",
                "id": "email"

            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name')
