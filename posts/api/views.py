from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from posts.api.serializers import PostSerializer
from posts.api.premissions import IsAuthorOrAdminOrReadOnly
from posts.models import Post


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
