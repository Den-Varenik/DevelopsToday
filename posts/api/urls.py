from django.urls import path

from posts.api import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="post-list"),
    path("<str:slug>/", views.PostDetailsView.as_view(), name="post-details"),
    path("<str:slug>/comments/", views.CommentListView.as_view(), name="comment-list"),
    path(
        "<str:slug>/comments/<int:pk>/",
        views.CommentDetailsView.as_view(),
        name="comment-details",
    ),
]
