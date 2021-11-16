from .models import Employee, Client
from django.forms import ModelForm


class EmployeeCreateForm(ModelForm):
    class Meta:
        model = Employee
        fields = ["initials", "fio", "dob", "photo", "organization", "position"]


class ClientCreateForm(ModelForm):
    class Meta:
        model = Client
        fields = ['fio', 'gender', 'dob', 'place', 'passport_series',
                  'passport_number', 'date_issue', 'date_end', 'issued_by', 'status', 'birth_certificate']
