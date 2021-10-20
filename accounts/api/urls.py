from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from accounts.api.views import logout_view, registration_view

urlpatterns = [
    path("login/", obtain_auth_token, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", registration_view, name="register"),
]
