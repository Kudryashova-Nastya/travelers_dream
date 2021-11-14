from django.shortcuts import render
from .models import Employee, Client
# from django.http import HttpResponse

def index(request):
    employees = Employee.objects.all()
    return render(request, 'travelers_dream/index.html', {'employees': employees})

def clients(request):
    clients = Client.objects.all()
    return render(request, 'travelers_dream/clients.html', {'clients': clients})

def create_employee(request):
    return render(request, 'travelers_dream/create_employee.html')
