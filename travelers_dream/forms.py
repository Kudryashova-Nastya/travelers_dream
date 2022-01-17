from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Employee, Client, AuthUser, Activity, Agreement, Contract, Payment
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


class AgreementCreateForm(ModelForm):
    class Meta:
        model = Agreement
        fields = ['date', 'organization', 'agent', 'client', 'number_participants', 'date_start',
                  'date_end', 'city']

class ContractCreateForm(ModelForm):
    class Meta:
        model = Contract
        fields = ['date', 'agreement_id']


class ContractUpdateForm(ModelForm):
    class Meta:
        model = Contract
        fields = ['organization', 'agent_id', 'sum', 'currency']


class PaymentCreateForm(ModelForm):
    class Meta:
        model = Payment
        fields = ['organization']


class StatusContractUpdateForm(ModelForm):
    class Meta:
        model = Contract
        fields = ['status']
