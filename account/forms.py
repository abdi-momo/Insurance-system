from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Mot de passe',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Retapez le mot de passe',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Nom d\'utilisateur ou mot de passe incorrecte')
        return cd['password2']

class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, label="Nom d'utilisateur")
    password = forms.CharField(max_length=20, label="Mot de passe", widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20, label="Confirmez le mot de passe", widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Les mots de passe ne correspondent pas")

        values = {
            "username": username,
            "password": password
        }
        return values


