import datetime

# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
# from .forms import UserRegistrationForm

from .models import Employee, Client, PositionEmployee, Organization, StatusClient, AuthUser
from .forms import EmployeeCreateForm, ClientCreateForm, UserCreateForm, AuthUserForm


# from django.http import HttpResponse

def index(request):
    search_query = request.GET.get('search', '')

    if search_query:
        employees = Employee.objects.filter(fio__icontains=search_query)
    else:
        employees = Employee.objects.all()
    return render(request, 'travelers_dream/index.html', {'employees': employees})


def clients(request):
    clients = Client.objects.all()
    return render(request, 'travelers_dream/clients.html', {'clients': clients})


def employee(request, id):
    error = ''
    person = Employee.objects.get(id=id)
    user = AuthUser.objects.get(id=person.user.id)
    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST, instance=person)
        if form.is_valid():
            a = form.save(commit=False)
            a.user = user
            a.save()
            return redirect('employees')
        else:
            error = 'Форма заполнена некорректно'

    positions = PositionEmployee.objects.all()
    organizations = Organization.objects.all()
    return render(request, 'travelers_dream/employee.html', {'employee': person, 'positions': positions,
                                                             'organizations': organizations, 'user': user,
                                                             'error': error})


def create_employee(request):
    error = ''
    if request.method == 'POST':
        last_id = AuthUser.objects.latest('id').id
        generate_username = 'user' + str(last_id)
        form_user = UserCreateForm(
            {'password': 'pbkdf2_sha256$260000$PSBgh7lmKJVRrRhjCbLKOy$PU2iKYptNwdOEquhRHuK2qxq9GbPBrPn/8NHOed9Jxg=',
             'last_login': str(datetime.datetime.now()), 'username': generate_username,
             'date_joined': str(datetime.datetime.now())})
        form = EmployeeCreateForm(request.POST)

        if form_user.is_valid() and form.is_valid():
            user_instance = form_user.save(commit=False)
            form_user.save()
            a = form.save(commit=False)
            a.user = user_instance
            a.save()
            return redirect('employees')
        else:
            error = str(form_user.errors) + str(form.errors)

    positions = PositionEmployee.objects.all()
    organizations = Organization.objects.all()
    return render(request, 'travelers_dream/create_employee.html', {'positions': positions,
                                                                    'organizations': organizations, 'error': error})


# def create_employee(request):
#     error = ''
#     if request.method == 'POST':
#         user_form = UserRegistrationForm(initial={'password': '12345', 'password2': '12345', 'username': 'user211',
#                                                   'first_name': ' ',
#                                                   'email': ' '})
#         if user_form.is_valid():
#             # Create a new user object but avoid saving it yet
#             new_user = user_form.save(commit=False)
#             # Set the chosen password
#             new_user.set_password(user_form.cleaned_data['password'])
#             # Save the User object
#             new_user.save()
#
#             form = EmployeeCreateForm(initial={'user': 'user211'}, instance=request.POST)
#             if form.is_valid():
#                 form.save(commit=False)
#                 return redirect('employees')
#             else:
#                 error = 'Форма заполнена некорректно'
#             return redirect('employees')
#         else:
#             error = str(user_form.errors)
#
#     positions = PositionEmployee.objects.all()
#     organizations = Organization.objects.all()
#     return render(request, 'travelers_dream/create_employee.html', {'positions': positions,
#                                                                     'organizations': organizations, 'error': error})
#


# def create_employee(request):
#     error = ''
#     if request.method == 'POST':
#         user_form = UserCreationForm({'username': 'user211', 'password': '12345', 'password2': '12345'})
#         if user_form.is_valid():
#             # Create a new user object but avoid saving it yet
#             new_user = user_form.save(commit=False)
#             # Set the chosen password
#             new_user.set_password(user_form.cleaned_data['password'])
#             # Save the User object
#             new_user.save()
#
#             form = EmployeeCreateForm(initial={'user': 'user211'}, instance=request.POST)
#             if form.is_valid():
#                 form.save()
#                 return redirect('employees')
#             else:
#                 error = 'Форма заполнена некорректно'
#             return redirect('employees')
#         else:
#             print(user_form.errors)
#             # return {}
#
#             error = str(user_form.errors)
#             # if error == '':
#             #     error = user_form.errors
#             #     if error == '':
#             #         error = 'бядааааа'
#
#     positions = PositionEmployee.objects.all()
#     organizations = Organization.objects.all()
#     return render(request, 'travelers_dream/create_employee.html', {'positions': positions,
#                                                                     'organizations': organizations, 'error': error})


def client(request, id):
    error = ''
    person = Client.objects.get(id=id)
    if request.method == 'POST':
        form = ClientCreateForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('clients')
        else:
            error = 'Форма заполнена некорректно'
    statuses = StatusClient.objects.all()
    return render(request, 'travelers_dream/client.html', {'client': person, 'statuses': statuses, 'error': error})


def create_client(request):
    error = ''
    if request.method == 'POST':
        form = ClientCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clients')
        else:
            error = 'Форма заполнена некорректно'

    statuses = StatusClient.objects.all()
    return render(request, 'travelers_dream/create_client.html', {'statuses': statuses, 'error': error})


class Login(LoginView):
    template_name = "travelers_dream/login.html"
    form_class = AuthUserForm
    success_url = reverse_lazy("employees")
