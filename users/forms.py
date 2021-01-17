from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    # one additional field
    email = forms.EmailField()

    # the model to be linked to and thee fields
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']