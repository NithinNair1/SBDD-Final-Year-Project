from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import queryToDoc


class CreateUser(UserCreationForm):
  class Meta:
    model = User
    fields = ['first_name','last_name','username','email','password1','password2']

class QueryUser(ModelForm):
  class Meta:
    model = queryToDoc
    fields = ['nickname','listosymp','predDiseases','note','mail']
    widgets = {
            'note': forms.Textarea(attrs={'placeholder': 'Enter your medical history and all details'}),
        }
