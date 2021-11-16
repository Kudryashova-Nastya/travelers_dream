from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.Login.as_view(), name="login"),
    path('employees', views.index, name="employees"),
    path('clients', views.clients, name="clients"),
    path('create-employee', views.create_employee, name="createEmployee"),
    path('employee/<int:id>', views.employee, name="employee"),
    path('create-client', views.create_client, name="createClient"),
    path('client/<int:id>', views.client, name="client"),
    # path('accounts/', include('django.contrib.auth.urls')),
]