from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import Employee, Client
from django.forms import ModelForm, forms


class EmployeeCreateForm(ModelForm):
    class Meta:
        model = Employee
        fields = ["initials", "fio", "dob", "photo", "organization", "position"]


class ClientCreateForm(ModelForm):
    class Meta:
        model = Client
        fields = ['fio', 'gender', 'dob', 'place', 'passport_series',
                  'passport_number', 'date_issue', 'date_end', 'issued_by', 'status', 'birth_certificate']


class AuthUserForm(AuthenticationForm, ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
