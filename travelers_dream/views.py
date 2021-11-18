from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Employee, Client, PositionEmployee, Organization, StatusClient
from .forms import EmployeeCreateForm, ClientCreateForm, AuthUserForm


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
    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('employees')
        else:
            error = 'Форма заполнена некорректно'

    positions = PositionEmployee.objects.all()
    organizations = Organization.objects.all()
    return render(request, 'travelers_dream/employee.html', {'employee': person, 'positions': positions,
                                                             'organizations': organizations, 'error': error})


# def create_employee(request):
#     form = EmployeeCreateForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'travelers_dream/create_employee.html', context)

def create_employee(request):
    error = ''
    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees')
        else:
            error = 'Форма заполнена некорректно'

    positions = PositionEmployee.objects.all()
    organizations = Organization.objects.all()
    return render(request, 'travelers_dream/create_employee.html', {'positions': positions,
                                                                    'organizations': organizations, 'error': error})


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





