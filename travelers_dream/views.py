from django.shortcuts import render, redirect
from .models import Employee, Client, PositionEmployee, Organization
from .forms import EmployeeCreateForm
# from django.http import HttpResponse

def index(request):
    employees = Employee.objects.all()
    return render(request, 'travelers_dream/index.html', {'employees': employees})

def clients(request):
    clients = Client.objects.all()
    return render(request, 'travelers_dream/clients.html', {'clients': clients})

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
    return render(request, 'travelers_dream/create_employee.html', {'positions': positions, 'organizations': organizations, 'error': error})