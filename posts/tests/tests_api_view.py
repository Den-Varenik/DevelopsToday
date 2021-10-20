from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from posts.models import Post, Comment, Upvote

User = get_user_model()


class PostsTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="example", password="Password@123"
        )
        self.author = User.objects.create_user(username="author", password="Author@123")
        self.post = Post.objects.create(
            author=self.author, title="Test title", link="https://www.google.com/"
        )

    def test_post_list(self):
        self._request_department(
            self.client.get, reverse("post-list"), status.HTTP_200_OK
        )

        token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        self._request_department(
            self.client.get, reverse("post-list"), status.HTTP_200_OK
        )

    def test_post_create(self):
        data = {"title": "Created title", "link": "https://www.google.com/"}

        self._request_department(
            self.client.post,
            reverse("post-list"),
            status.HTTP_401_UNAUTHORIZED,
            data=data,
        )

        token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        self._request_department(
            self.client.post, reverse("post-list"), status.HTTP_201_CREATED, data=data
        )
        self.assertEqual(Post.objects.all().count(), 2)

    def test_post_retrieve(self):
        self._request_department(
            self.client.get,
            reverse("post-details", kwargs={"slug": self.post.slug}),
            status.HTTP_200_OK,
        )

        token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        self._request_department(
            self.client.get,
            reverse("post-details", kwargs={"slug": self.post.slug}),
            status.HTTP_200_OK,
        )

    def test_post_update(self):
        data = {"title": "Updated title", "link": "https://www.google.com/"}

        self._request_department(
            self.client.put,
            reverse("post-details", kwargs={"slug": self.post.slug}),
            status.HTTP_401_UNAUTHORIZED,
            data=data,
        )

        token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        self._request_department(
            self.client.put,
            reverse("post-details", kwargs={"slug": self.post.slug}),
            status.HTTP_403_FORBIDDEN,
            data=data,
        )

        token = Token.objects.get(user__username=self.author)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        self._request_department(
            self.client.put,
            reverse("post-details", kwargs={"slug": self.post.slug}),
            status.HTTP_200_OK,
            data=data,
        )

    def test_post_delete(self):
        self._request_department(
            self.client.delete,
            reverse("post-details", kwargs={"slug": self.post.slug}),
            status.HTTP_401_UNAUTHORIZED,
        )

        token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        self._request_department(
            self.client.delete,
            reverse("post-details", kwargs={"slug": self.post.slug}),
            status.HTTP_403_FORBIDDEN,
        )

        token = Token.objects.get(user__username=self.author)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        self._request_department(
            self.client.delete,
            reverse("post-details", kwargs={"slug": self.post.slug}),
            status.HTTP_204_NO_CONTENT,
        )

    def _request_department(self, method, path, status_code, data: dict = None) -> None:
        response = method(path, data, format="json")
        self.assertEqual(response.status_code, status_code)


class CommentTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="example", password="Password@123"
        )
        self.author = User.objects.create_user(username="author", password="Author@123")
        self.post = Post.objects.create(
            author=self.author, title="Test title", link="https://www.google.com/"
        )
        self.comment = Comment.objects.create(
            author=self.author, post=self.post, content="Test comment"
        )

    def test_comment_list(self):
        self._request_department(
            self.client.get,
            reverse("comment-list", kwargs={"slug": self.post.slug}),
            status.HTTP_200_OK,
        )

        token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        self._request_department(
            self.client.get,
            reverse("comment-list", kwargs={"slug": self.post.slug}),
            status.HTTP_200_OK,
        )

    def test_comment_create(self):
        data = {"content": "Created comment"}

        self._request_department(
            self.client.post,
            reverse("comment-list", kwargs={"slug": self.post.slug}),
            status.HTTP_401_UNAUTHORIZED,
            data=data,
        )

        token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        self._request_department(
            self.client.post,
            reverse("comment-list", kwargs={"slug": self.post.slug}),
            status.HTTP_201_CREATED,
            data=data,
        )
        self.assertEqual(self.post.comments.count(), 2)

    def test_comment_retrieve(self):
        self._request_department(
            self.client.get,
            reverse(
                "comment-details",
                kwargs={"slug": self.post.slug, "pk": self.comment.pk},
            ),
            status.HTTP_200_OK,
        )

        token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        self._request_department(
            self.client.get,
            reverse(
                "comment-details",
                kwargs={"slug": self.post.slug, "pk": self.comment.pk},
            ),
            status.HTTP_200_OK,
        )

    def test_comment_update(self):
        data = {"content": "Updated comment"}

        self._request_department(
            self.client.put,
            reverse(
                "comment-details",
                kwargs={"slug": self.post.slug, "pk": self.comment.pk},
            ),
            status.HTTP_401_UNAUTHORIZED,
            data=data,
        )

        token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        self._request_department(
            self.client.put,
            reverse(
                "comment-details",
                kwargs={"slug": self.post.slug, "pk": self.comment.pk},
            ),
            status.HTTP_403_FORBIDDEN,
            data=data,
        )

        token = Token.objects.get(user__username=self.author)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        self._request_department(
            self.client.put,
            reverse(
                "comment-details",
                kwargs={"slug": self.post.slug, "pk": self.comment.pk},
            ),
            status.HTTP_200_OK,
            data=data,
        )
        self.assertEqual(
            Comment.objects.get(pk=self.comment.pk).content, "Updated comment"
        )

    def test_comment_delete(self):
        self._request_department(
            self.client.delete,
            reverse(
                "comment-details",
                kwargs={"slug": self.post.slug, "pk": self.comment.pk},
            ),
            status.HTTP_401_UNAUTHORIZED,
        )

        token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        self._request_department(
            self.client.delete,
            reverse(
                "comment-details",
                kwargs={"slug": self.post.slug, "pk": self.comment.pk},
            ),
            status.HTTP_403_FORBIDDEN,
        )

        token = Token.objects.get(user__username=self.author)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        self._request_department(
            self.client.delete,
            reverse(
                "comment-details",
                kwargs={"slug": self.post.slug, "pk": self.comment.pk},
            ),
            status.HTTP_204_NO_CONTENT,
        )
        self.assertEqual(Comment.objects.all().count(), 0)

    def _request_department(self, method, path, status_code, data: dict = None) -> None:
        response = method(path, data, format="json")
        self.assertEqual(response.status_code, status_code)


class UpvoteTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="example", password="Password@123"
        )
        self.post = Post.objects.create(
            author=self.user, title="Test title", link="https://www.google.com/"
        )
        self.upvote = Upvote.objects.create(user=self.user, post=self.post)

    def test_upvote_list(self):
        self._request_department(
            self.client.get,
            reverse("upvote-list", kwargs={"slug": self.post.slug}),
            status.HTTP_401_UNAUTHORIZED,
        )

        token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        self._request_department(
            self.client.get,
            reverse("upvote-list", kwargs={"slug": self.post.slug}),
            status.HTTP_403_FORBIDDEN,
        )

    def test_upvote_create(self):
        self._request_department(
            self.client.post,
            reverse("upvote-list", kwargs={"slug": self.post.slug}),
            status.HTTP_401_UNAUTHORIZED,
        )

        token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        self._request_department(
            self.client.post,
            reverse("upvote-list", kwargs={"slug": self.post.slug}),
            status.HTTP_201_CREATED,
        )
        self.assertEqual(self.post.upvote.count(), 2)

    def test_upvote_retrieve(self):
        self._request_department(
            self.client.get,
            reverse(
                "upvote-details",
                kwargs={"slug": self.post.slug, "pk": self.upvote.pk},
            ),
            status.HTTP_401_UNAUTHORIZED,
        )

        token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        self._request_department(
            self.client.get,
            reverse(
                "upvote-details",
                kwargs={"slug": self.post.slug, "pk": self.upvote.pk},
            ),
            status.HTTP_403_FORBIDDEN,
        )

    def test_upvote_delete(self):
        self._request_department(
            self.client.delete,
            reverse(
                "upvote-details",
                kwargs={"slug": self.post.slug, "pk": self.upvote.pk},
            ),
            status.HTTP_401_UNAUTHORIZED,
        )

        token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        self._request_department(
            self.client.delete,
            reverse(
                "upvote-details",
                kwargs={"slug": self.post.slug, "pk": self.upvote.pk},
            ),
            status.HTTP_204_NO_CONTENT,
        )

    def _request_department(self, method, path, status_code, data: dict = None) -> None:
        response = method(path, data, format="json")
        self.assertEqual(response.status_code, status_code)
