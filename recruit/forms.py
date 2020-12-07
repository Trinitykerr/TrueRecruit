from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Contact, PlayerMore, CoachMore
from django.forms import widgets


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required. Add a vaild email address')

    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2", "type")


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'age', 'message']


class CreatePlayer(forms.ModelForm):


    class Meta:
        model = PlayerMore
        fields = ['user','email', 'name', 'image', 'age', 'state', 'city', 'position', 'club', 'school', 'gradyear', 'gpa', 'height', 'weight',
                  'phone', 'summary', 'skills']


class CreateCoach(forms.ModelForm):



    class Meta:
        model = CoachMore
        fields = ['user', 'email', 'name', 'image','state', 'position', 'school', 'experience', 'requirements', 'phone']
        readonly = ('user', 'email')



class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


