from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Employee, Client, AuthUser, Activity
from django.forms import ModelForm, forms, CharField, PasswordInput, TextInput


class EmployeeCreateForm(ModelForm):
    class Meta:
        model = Employee
        fields = ["initials", "fio", "dob", "photo", "organization", "position", "user"]


class ClientCreateForm(ModelForm):
    class Meta:
        model = Client
        fields = ['fio', 'gender', 'dob', 'place', 'passport_series',
                  'passport_number', 'date_issue', 'date_end', 'issued_by', 'status', 'birth_certificate']


class AuthUserForm(AuthenticationForm, ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class UserCreateForm(ModelForm):
    class Meta:
        model = AuthUser
        fields = ['password', 'last_login', 'username', 'date_joined']

class UserActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = ['user_id', 'date', 'time', 'day_activity', 'night_activity']


# class UserRegistrationForm(ModelForm):
#     username = CharField(label='Username', widget=TextInput)
#     password1 = CharField(label='Password', widget=PasswordInput)
#     password2 = CharField(label='Repeat password', widget=PasswordInput)
#
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'email')
#
#     def clean_password2(self):
#         cd = self.cleaned_data
#         if cd['password1'] != cd['password2']:
#             raise ValidationError('Passwords don\'t match.')
#         return cd['password2']
