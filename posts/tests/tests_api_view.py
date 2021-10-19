from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Post

User = get_user_model()


class PostsTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.author = User.objects.create_user(username="author", password="Author@123")
        self.post = Post.objects.create(author=self.author, title="Test title", link="https://www.google.com/")

    def test_post_list(self):
        self.client.login(username="example", password="Password@123")
        self._request_department(self.client.get, reverse('post-list'), status.HTTP_200_OK)

        self.client.logout()
        self._request_department(self.client.get, reverse('post-list'), status.HTTP_200_OK)

    def test_post_create(self):
        data = {"title": "Created title", "link": "https://www.google.com/"}

        self.client.login(username="example", password="Password@123")
        self._request_department(self.client.post, reverse('post-list'), status.HTTP_201_CREATED, data=data)
        self.assertEqual(Post.objects.all().count(), 2)

        self.client.logout()
        self._request_department(self.client.post, reverse('post-list'), status.HTTP_403_FORBIDDEN, data=data)

    def test_post_retrieve(self):
        self.client.login(username="example", password="Password@123")
        self._request_department(self.client.get, reverse('post-details', kwargs={"pk": self.post.pk}), status.HTTP_200_OK)

        self.client.logout()
        self._request_department(self.client.get, reverse('post-details', kwargs={"pk": self.post.pk}), status.HTTP_200_OK)

    def test_post_update(self):
        data = {"title": "Updated title", "link": "https://www.google.com/"}

        self.client.login(username="example", password="Password@123")
        self._request_department(self.client.put, reverse('post-details', kwargs={"pk": self.post.pk}), status.HTTP_403_FORBIDDEN, data=data)

        self.client.logout()
        self._request_department(self.client.put, reverse('post-details', kwargs={"pk": self.post.pk}), status.HTTP_403_FORBIDDEN, data=data)

        self.client.login(username="author", password="Author@123")
        self._request_department(self.client.put, reverse('post-details', kwargs={"pk": self.post.pk}), status.HTTP_200_OK, data=data)

    def test_post_delete(self):
        self.client.login(username="example", password="Password@123")
        self._request_department(self.client.delete, reverse('post-details', kwargs={"pk": self.post.pk}), status.HTTP_403_FORBIDDEN)

        self.client.logout()
        self._request_department(self.client.delete, reverse('post-details', kwargs={"pk": self.post.pk}), status.HTTP_403_FORBIDDEN)

        self.client.login(username="author", password="Author@123")
        self._request_department(self.client.delete, reverse('post-details', kwargs={"pk": self.post.pk}),
                                 status.HTTP_204_NO_CONTENT)

    def _request_department(self, method, path, status_code, data: dict = None) -> None:
        response = method(path, data, format="json")
        self.assertEqual(response.status_code, status_code)
