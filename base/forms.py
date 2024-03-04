from dataclasses import fields
from pyexpat import model
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms


class createUserForm(UserCreationForm):
    class Meta:
        model= CustomUser
        fields = ('email', 'password1', 'password2', 'is_parent', 'is_guardian', 'is_law_enforcer')
    



        