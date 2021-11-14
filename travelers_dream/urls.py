from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="employees"),
    path('clients', views.clients, name="clients"),
    path('create-employee', views.create_employee, name="createEmployee"),
]