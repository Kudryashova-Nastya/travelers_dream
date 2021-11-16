from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('travelers_dream.urls')),
    path('login/', LoginView.as_view(), name='login'),
]
