from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Post, Comment, User
from api.serializers import (
    PostWriteSerializer,
    UserSerializer,
    PostReadSerializer,
    CommentReadSerializer
)


class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(
            author=self.user,
            content='Test post content'
        )
        self.comment = Comment.objects.create(
            author=self.user,
            post=self.post,
            content='Test comment content'
        )

    def test_create_user(self):
        url = reverse('user-list')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newuserpassword',
            'followers': [1]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_user = User.objects.get(username=data['username'])
        self.assertEqual(new_user.username, data['username'])

    def test_create_post(self):
        url = reverse('post-list')
        data = {
            'author': self.user.pk,
            'content': 'New post content'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_post = Post.objects.get(content=data['content'])
        self.assertEqual(new_post.content, data['content'])

    def test_create_comment(self):
        url = reverse('comment-list', kwargs={'pk': self.post.pk})
        data = {
            'author': self.user.pk,
            'post': self.post.pk,
            'content': 'New comment content'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_comment = Comment.objects.get(content=data['content'])
        self.assertEqual(new_comment.content, data['content'])

    def test_follow_user(self):
        random_name = 'randomstring'
        user_to_follow = User.objects.create_user(
            username=random_name,
            email='user2@example.com',
            password='password2'
        )
        url = reverse(
            'user-follow', kwargs={'pk': self.user.pk, 'follow_id': user_to_follow.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(user_to_follow, self.user.following.all())

    def test_get_user_details(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = UserSerializer(self.user)
        self.assertEqual(response.data, serializer.data)

    def test_get_all_users(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_post_details(self):
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = PostReadSerializer(self.post)
        self.assertEqual(response.data, serializer.data)

    def test_get_post_comments(self):
        url = reverse('comment-list', kwargs={'pk': self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comments = Comment.objects.filter(
            post=self.post).order_by('-created_at')
        serializer = CommentReadSerializer(comments, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_all_posts(self):
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        posts = Post.objects.all().order_by('-created_at')
        serializer = PostWriteSerializer(posts, many=True)
        self.assertEqual(response.data, serializer.data)
