from django.shortcuts import render, redirect
from .models import Employee, Client, PositionEmployee, Organization, StatusClient
from .forms import EmployeeCreateForm, ClientCreateForm


# from django.http import HttpResponse

def index(request):
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





