import datetime

# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
# from .forms import UserRegistrationForm

from .models import Employee, Client, PositionEmployee, Organization, StatusClient, AuthUser, Activity, Agreement, City, \
    Contract, Currency
from .forms import EmployeeCreateForm, ClientCreateForm, UserCreateForm, AuthUserForm, UserActivityForm, \
    AgreementCreateForm, ContractCreateForm, ContractUpdateForm


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
    employee = Employee.objects.get(id=id)
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
            error = str(form_employee.errors)
    user = AuthUser.objects.get(id=employee.user.id)
    positions = PositionEmployee.objects.all()
    organizations = Organization.objects.all()

    # кол-во активностей за день
    activities = Activity.objects.filter(user_id=employee.id, date=str(datetime.datetime.now().date())).count()

    # статус пользователя (сова или жаворонок) определяется в зависимости от того, в какое время был наиболее активен пользователь за текущий месяц
    month_activities_daytime = Activity.objects.filter(user_id=employee.id, day_activity=True,
                                                       date__contains='-' + str(
                                                           datetime.datetime.now().date().strftime('%m')) + '-').count()
    month_activities_nighttime = Activity.objects.filter(user_id=employee.id, night_activity=True,
                                                         date__contains='-' + str(
                                                             datetime.datetime.now().date().strftime(
                                                                 '%m')) + '-').count()
    if month_activities_daytime > month_activities_nighttime:
        status = 'жаворонок'
    elif month_activities_daytime < month_activities_nighttime:
        status = 'сова'
    else:
        status = 'не определился'

    return render(request, 'travelers_dream/employee.html', {'employee': employee, 'positions': positions,
                                                             'organizations': organizations, 'user': user,
                                                             'activities': activities, 'status': status,
                                                             'daytime': month_activities_daytime, 'error': error,
                                                             'nighttime': month_activities_nighttime})


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
        # добавление активности пользователя
        try:
            employee = Employee.objects.get(user=request.user.id)
        except Employee.DoesNotExist:
            employee = None

        if employee is not None:
            if 6 <= datetime.datetime.now().hour < 18:
                form_activity = UserActivityForm(
                    {'user_id': employee.id, 'date': str(datetime.datetime.now().date()),
                     'time': str(datetime.datetime.now().time()),
                     'day_activity': True, 'night_activity': False})
            else:
                form_activity = UserActivityForm(
                    {'user_id': employee.id, 'date': str(datetime.datetime.now().date()),
                     'time': str(datetime.datetime.now().time()),
                     'day_activity': False, 'night_activity': True})
            if form_activity.is_valid():
                form_activity.save()

        form = ClientCreateForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('clients')
        else:
            error = str(form.errors)
    statuses = StatusClient.objects.all()
    return render(request, 'travelers_dream/client.html', {'client': person, 'statuses': statuses, 'error': error})


def create_client(request):
    error = ''
    if request.method == 'POST':
        # добавление активности пользователя
        try:
            employee = Employee.objects.get(user=request.user.id)
        except Employee.DoesNotExist:
            employee = None

        if employee is not None:
            if 6 <= datetime.datetime.now().hour < 18:
                form_activity = UserActivityForm(
                    {'user_id': employee.id, 'date': str(datetime.datetime.now().date()),
                     'time': str(datetime.datetime.now().time()),
                     'day_activity': True, 'night_activity': False})
            else:
                form_activity = UserActivityForm(
                    {'user_id': employee.id, 'date': str(datetime.datetime.now().date()),
                     'time': str(datetime.datetime.now().time()),
                     'day_activity': False, 'night_activity': True})
            if form_activity.is_valid():
                form_activity.save()

        form = ClientCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clients')
        else:
            error = str(form.errors)

    statuses = StatusClient.objects.all()
    return render(request, 'travelers_dream/create_client.html', {'statuses': statuses, 'error': error})


def agreements(request):
    agreements = Agreement.objects.all()
    return render(request, 'travelers_dream/agreements.html', {'agreements': agreements})


def agreement(request, id):
    error = ''
    agreement = Agreement.objects.get(id=id)
    if request.method == 'POST':
        # добавление активности пользователя
        try:
            employee = Employee.objects.get(user=request.user.id)
        except Employee.DoesNotExist:
            employee = None
        if employee is not None:
            if 6 <= datetime.datetime.now().hour < 18:
                form_activity = UserActivityForm(
                    {'user_id': employee.id, 'date': str(datetime.datetime.now().date()),
                     'time': str(datetime.datetime.now().time()),
                     'day_activity': True, 'night_activity': False})
            else:
                form_activity = UserActivityForm(
                    {'user_id': employee.id, 'date': str(datetime.datetime.now().date()),
                     'time': str(datetime.datetime.now().time()),
                     'day_activity': False, 'night_activity': True})
            if form_activity.is_valid():
                form_activity.save()

        form = AgreementCreateForm(request.POST, instance=agreement)
        if form.is_valid():
            form.save()
            if 'update' in request.POST:
                return redirect('agreements')
            elif 'update_redirect' in request.POST:
                # проверяем существует ли связанный договор
                try:
                    contract = Contract.objects.get(agreement_id=agreement)
                except Contract.DoesNotExist:
                    contract = None

                # если договор существует, переходим к нему
                # иначе создаём договор и редиректим на него
                if contract is None:
                    form_contractCreate = ContractCreateForm(
                        {'date': str(datetime.datetime.now().date()),
                         'agreement_id': agreement})
                    if form_contractCreate.is_valid():
                        contract_instance = form_contractCreate.save(commit=False)
                        contract_instance.save()
                        return redirect('contract', id=contract_instance.id)
                    else:
                        error = str(form_contractCreate.errors)
                else:
                    return redirect('contract', id=contract.id)
            return redirect('agreements')
        else:
            error = str(form.errors)

    organizations = Organization.objects.all()
    agent = Employee.objects.all()
    client = Client.objects.all()
    city = City.objects.all()
    return render(request, 'travelers_dream/agreement.html',
                  {'agreement': agreement, 'error': error, 'organizations': organizations, 'agent': agent,
                   'client': client, 'city': city})


def create_agreement(request):
    error = ''
    if request.method == 'POST':
        # добавление активности пользователя
        try:
            employee = Employee.objects.get(user=request.user.id)
        except Employee.DoesNotExist:
            employee = None

        if employee is not None:
            if 6 <= datetime.datetime.now().hour < 18:
                form_activity = UserActivityForm(
                    {'user_id': employee.id, 'date': str(datetime.datetime.now().date()),
                     'time': str(datetime.datetime.now().time()),
                     'day_activity': True, 'night_activity': False})
            else:
                form_activity = UserActivityForm(
                    {'user_id': employee.id, 'date': str(datetime.datetime.now().date()),
                     'time': str(datetime.datetime.now().time()),
                     'day_activity': False, 'night_activity': True})
            if form_activity.is_valid():
                form_activity.save()

        form = AgreementCreateForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.date = datetime.datetime.now().date()
            form_instance.save()
            if 'add' in request.POST:
                return redirect('agreements')
            elif 'add_redirect' in request.POST:
                # создаём договор и редиректим на него
                form_contractCreate = ContractCreateForm(
                    {'date': str(datetime.datetime.now().date()),
                     'agreement_id': form_instance.id})
                if form_contractCreate.is_valid():
                    contract_instance = form_contractCreate.save(commit=False)
                    contract_instance.save()
                    return redirect('contract', id=contract_instance.id)
                else:
                    error = str(form_contractCreate.errors)
        else:
            error = str(form.errors)

    organizations = Organization.objects.all()
    agent = Employee.objects.all()
    client = Client.objects.all()
    city = City.objects.all()
    return render(request, 'travelers_dream/create_agreement.html',
                  {'error': error, 'organizations': organizations, 'agent': agent, 'client': client, 'city': city})


def contracts(request):
    contracts = Contract.objects.all()
    return render(request, 'travelers_dream/contracts.html', {'contracts': contracts})


def contract(request, id):
    error = ''
    contract = Contract.objects.get(id=id)
    if request.method == 'POST':
        # добавление активности пользователя
        try:
            employee = Employee.objects.get(user=request.user.id)
        except Employee.DoesNotExist:
            employee = None
        if employee is not None:
            if 6 <= datetime.datetime.now().hour < 18:
                form_activity = UserActivityForm(
                    {'user_id': employee.id, 'date': str(datetime.datetime.now().date()),
                     'time': str(datetime.datetime.now().time()),
                     'day_activity': True, 'night_activity': False})
            else:
                form_activity = UserActivityForm(
                    {'user_id': employee.id, 'date': str(datetime.datetime.now().date()),
                     'time': str(datetime.datetime.now().time()),
                     'day_activity': False, 'night_activity': True})
            if form_activity.is_valid():
                form_activity.save()

        form = ContractUpdateForm(request.POST, instance=contract)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.date = datetime.datetime.now().date()
            form_instance.agreement_id = contract.agreement_id
            form_instance.status = 'Ожидание оплаты поездки'
            form_instance.save()
            return redirect('contracts')
        else:
            error = str(form.errors)

    organizations = Organization.objects.all()
    agent = Employee.objects.all()
    currency = Currency.objects.all()
    city = City.objects.all()
    return render(request, 'travelers_dream/contract.html',
                  {'contract': contract, 'error': error, 'organizations': organizations, 'agent': agent,
                   'city': city, 'currency': currency})


class Login(LoginView):
    template_name = "travelers_dream/login.html"
    form_class = AuthUserForm
    success_url = reverse_lazy("employees")
