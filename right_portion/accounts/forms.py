from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField

from right_portion.accounts.models import RPUser


# Create your forms here.


class RPUserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = RPUser
        fields = ('username', 'email')
        widgets = {'username': forms.TextInput()}


class RPUserEditForm(forms.ModelForm):
    class Meta:
        model = RPUser
        fields = ('username', 'email', 'profile_picture')
        exclude = ('password',)
        labels = {
            'username': 'Username:',
            'email': 'Email:',
            'profile_picture': 'Profile Pic:'
        }


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True, "placeholder": "Username"}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "placeholder": "Password"}))