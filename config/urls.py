from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/post/", include("posts.api.urls")),
]
