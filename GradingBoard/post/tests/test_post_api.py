"""
Test for recipe APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Post,
)

from post.serializers import (
    PostSerializer,
    # SchoolSerializer,
    # FacultySerializer,
    # ClassSerializer,
    # ProfessorSerializer,
    # CommentSerializer,
)


POST_URL = reverse('post:post-list')


def detail_url(post_id):
    """ Create and return a post detail URL. """
    return reverse('post:post-detail', args=[post_id])


def create_post(user, school=1, faculty=1, _class=1, professor=1, **paramas):
    """ Create and return a sample recipe. """
    defaults = {
        'quality': 3,
        'difficulty': 3,
        'recommend': True,
        'created_at': timezone.now(),
        'modified_at': timezone.now(),
    }
    # If we provide some params, then we apply that params
    defaults.update(paramas)

    post = Post.objects.create(user=user, school=school, _class=_class, professor=professor, **defaults)
    return post


def create_user(**params):
    """ Create and return a new user. """
    return get_user_model().objects.create_user(**params)


class PublicPostAPITest(TestCase):
    """ Test unauthenticated API requests. """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """ Test auth is required to call API. """
        res = self.client.get(POST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePostApiTest(TestCase):
    """ Test authenticated API requests. """

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """ Test retrieving a list of posts. """
        pass

    def test_post_limited_to_user(self):
        """ Test list of post is limited to authenticated user. """
        pass

    def test_get_post_detail(self):
        """ Test get post detail. """
        pass

    def test_create_post(self):
        """ Test creating a post. """
        pass

    def test_partial_update(self):
        """ Test partial update of a post. """
        pass

    def test_full_update(self):
        """ Test full update of a post. """
        pass

    def test_update_user_return_error(self):
        """ Test changing the post user results in an error. """
        pass

    def test_delete_post(self):
        pass

    def test_post_other_users_post_error(self):
        pass
