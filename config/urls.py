from django.conf import settings
from django.contrib import admin
from django.urls import path

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
]
