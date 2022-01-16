from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login', views.Login.as_view(), name="login"),
    path('logout', LogoutView.as_view(next_page="login"), name='logout'),
    path('', views.index, name="employees"),
    path('clients', views.clients, name="clients"),
    path('create-employee', views.create_employee, name="createEmployee"),
    path('employee/<int:id>', views.employee, name="employee"),
    path('create-client', views.create_client, name="createClient"),
    path('client/<int:id>', views.client, name="client"),
    path('agreements', views.agreements, name="agreements"),
    path('agreement/<int:id>', views.agreement, name="agreement"),
    path('create-agreement', views.create_agreement, name="createAgreement"),
]
