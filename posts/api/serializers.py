from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    upvote = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
