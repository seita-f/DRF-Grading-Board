"""
Test for models
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from core import models


def create_user(email='user@example.com', password='pass123'):
    """ Creat and return a user """
    return get_user_model().objects.create_user(email, password)


class PropertyTests(TestCase):
    """ Test creating School, Faculty, Class and Professor """

    def test_create_school(self):
        """ Test creating schools """
        school = models.School.objects.create(name='University XXX')

        self.assertEqual(str(school), school.name)

    def test_create_faculty(self):
        """ Test creating faculties """
        school = models.School.objects.create(name='University XXX')
        faculty = models.Faculty.objects.create(school=school, name='Faculty XYZ')

        self.assertEqual(str(faculty), faculty.name)

    def test_create_class(self):
        """ Test creating classes """
        school = models.School.objects.create(name='University XXX')
        faculty = models.Faculty.objects.create(school=school, name='Faculty XYZ')
        class_obj = models.Class.objects.create(faculty=faculty, name='Class ABC')

        self.assertEqual(str(class_obj), class_obj.name)

    def test_create_professor(self):
        """ Test creating professors """
        school = models.School.objects.create(name='University XXX')
        faculty = models.Faculty.objects.create(school=school, name='Faculty XYZ')
        professor = models.Professor.objects.create(faculty=faculty, name='Professor PQR')

        self.assertEqual(str(professor), professor.name)


class ModelsTest(TestCase):
    """ Test Models """

    def test_create_user_with_email_successful(self):
        email = "123@example.com"
        password = "password"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


    def test_new_user_email_normalized(self):
        """ Test email is normalized for new users. """
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'password')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """ Test that creating a user without an email raises a Value Error. """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'password')

    def test_create_superuser(self):
        """ Test creating a superuser """
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'password',
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_post(self):
        """ Test creating a post is successful """
        user = get_user_model().objects.create_user(
            'test@example.com',
            'pass123',
        )
        post = models.Post.objects.create(
            user=user,
            description='Description',
            school=models.School.objects.create(name='University XYZ'),
            faculty=models.Faculty.objects.create(school_id=1, name='Faculty ABC'),
            _class=models.Class.objects.create(faculty_id=1, name='Class DEF'),
            professor=models.Professor.objects.create(faculty_id=1, name='Professor GHI'),
            quality=5,
            difficulty=3,
            recommend=True,
            created_at=timezone.now(),
            modified_at=timezone.now(),
        )

        self.assertEqual(str(post), post.description[:25])

    def test_create_comment(self):
        """ Test creating a comment is successful """
        user = get_user_model().objects.create_user(
            'test@example.com',
            'pass123',
        )
        user2 = get_user_model().objects.create_user(
            'test2@example.com',
            'pass123',
        )
        post = models.Post.objects.create(
            user=user,
            description='Description',
            school=models.School.objects.create(name='University XYZ'),
            faculty=models.Faculty.objects.create(school_id=1, name='Faculty ABC'),
            _class=models.Class.objects.create(faculty_id=1, name='Class DEF'),
            professor=models.Professor.objects.create(faculty_id=1, name='Professor GHI'),
            quality=5,
            difficulty=3,
            recommend=True,
            created_at=timezone.now(),
            modified_at=timezone.now(),
        )
        comment = models.Comment.objects.create(
            user = user2,
            post = post,
            text = 'This is a comment in a post',
            created_at=timezone.now(),
            modified_at=timezone.now(),
        )

        self.assertEqual(str(comment), comment.text[:25])
