from django.urls import path

from posts.api import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="post-list"),
    path("<int:pk>/", views.PostDetailsView.as_view(), name="post-details"),
]
