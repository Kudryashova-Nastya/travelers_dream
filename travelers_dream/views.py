import datetime

# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.db import transaction
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
    if request.method == 'POST':
        form_employee = EmployeeCreateForm(request.POST, instance=employee)
        if form_employee.is_valid():
            with transaction.atomic():
                person = Employee.objects.get(id=id)
                user = AuthUser.objects.get(id=person.user.id)
                employee_instance = form_employee.save(commit=False)
                employee_instance.user = user
                employee_instance.save()
            return redirect('employees')
        else:
            error = 'Форма заполнена некорректно'
    employee = Employee.objects.get(id=id)
    user = AuthUser.objects.get(id=employee.user.id)
    positions = PositionEmployee.objects.all()
    organizations = Organization.objects.all()
    return render(request, 'travelers_dream/employee.html', {'employee': employee, 'positions': positions,
                                                             'organizations': organizations, 'user': user,
                                                             'error': error})


def create_employee(request):
    error = ''
    double = ''
    if request.method == 'POST':
        check_unique = Employee.objects.filter(fio=request.POST['fio'], initials=request.POST['initials'],
                                               dob=request.POST['dob'], position=request.POST['position']).exists()
        if check_unique:
            double = Employee.objects.filter(fio=request.POST['fio'], initials=request.POST['initials'],
                                             dob=request.POST['dob'], position=request.POST['position']).latest('id')

        if not check_unique or 'double' in request.POST:
            req = request.POST.copy()
            if 'double' in request.POST:
                req.pop('double')
            last_id = AuthUser.objects.latest('id').id
            generate_username = 'user' + str(last_id)
            form_user = UserCreateForm(
                {'password': 'pbkdf2_sha256$260000$PSBgh7lmKJVRrRhjCbLKOy$PU2iKYptNwdOEquhRHuK2qxq9GbPBrPn/8NHOed9Jxg=',
                 'last_login': str(datetime.datetime.now()), 'username': generate_username,
                 'date_joined': str(datetime.datetime.now())})
            form_employee = EmployeeCreateForm(req)

            if form_user.is_valid() and form_employee.is_valid():
                with transaction.atomic():
                    user_instance = form_user.save(commit=False)
                    form_user.save()
                    employee_instance = form_employee.save(commit=False)
                    employee_instance.user = user_instance
                    employee_instance.save()
                return redirect('employees')
            else:
                error = str(form_user.errors) + str(form_employee.errors)
        else:
            error = 'Сотрудник с такими же данными уже существует. Выберите филиал и повторите отправку данных, если всё же хотите внести его в базу'

    positions = PositionEmployee.objects.all()
    organizations = Organization.objects.all()
    return render(request, 'travelers_dream/create_employee.html',
                  {'positions': positions, 'organizations': organizations, 'error': error, 'init': double})


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
