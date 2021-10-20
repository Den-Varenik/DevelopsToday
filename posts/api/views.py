from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from posts.api.serializers import PostSerializer, CommentSerializer, UpvoteSerializer
from posts.api.premissions import IsAuthorOrAdminOrReadOnly, IsAuthenticatedOrAdmin
from posts.models import Post, Comment, Upvote


class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly]
    lookup_field = "slug"


class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_slug = self.kwargs["slug"]
        return Comment.objects.filter(post__slug=post_slug)

    def perform_create(self, serializer):
        post_slug = self.kwargs["slug"]
        post = Post.objects.get(slug=post_slug)
        serializer.save(author=self.request.user, post=post)


class CommentDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly]


class UpvoteListView(generics.ListCreateAPIView):
    serializer_class = UpvoteSerializer
    permission_classes = [IsAuthenticatedOrAdmin]

    def get_queryset(self):
        post_slug = self.kwargs["slug"]
        return Upvote.objects.filter(post__slug=post_slug)

    def perform_create(self, serializer):
        post_slug = self.kwargs["slug"]
        post = Post.objects.get(slug=post_slug)
        serializer.save(user=self.request.user, post=post)


class UpvoteDetailsView(generics.RetrieveDestroyAPIView):
    queryset = Upvote.objects.all()
    serializer_class = UpvoteSerializer
    permission_classes = [IsAuthenticatedOrAdmin]
