"""
Database models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

##### USER MODEL #####
class UserManager(BaseUserManager):
    """ Manger User """
    def create_user(self, email, password=None, **extra_fields):

        """ Create, save and return a new user. """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        """ Create, save and return a new superuser. """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ User in the system """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False) # Login with Django Admin
    is_active = models.BooleanField(default=True) # Login with Django Admin
    objects = UserManager()

    # Specifies that the email field is used as the unique identifier for authentication
    USERNAME_FIELD = 'email'


##### Define field by superuser #####
# School -> Faculty -> Class & Professor
class School(models.Model):
    """ School """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Faculty(models.Model):
    """ School -> Faculty  """
    name = models.CharField(max_length=255, unique=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Class(models.Model):
    """ Faculty -> Class """
    name = models.CharField(max_length=255, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Professor(models.Model):
    """ Faculty -> Class """
    name = models.CharField(max_length=255, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


##### POST MODEL #####
class Post(models.Model):
    """ Post object """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    # user can choose those fields
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    quality = models.IntegerField(choices=zip(range(1, 6), range(1, 6)))
    difficulty = models.IntegerField(choices=zip(range(1, 6), range(1, 6)))
    recommend = models.BooleanField(default=False) # Yes or No

    # fill manually
    description = models.TextField(blank=True)

    # auto fill
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    modified_at = models.DateTimeField(editable=False, blank=True, auto_now=True)  # auto_now => called everytime save() is called

    def __str__(self):
        return self.description[:25]


##### COMMENT MODEL #####
class Comment(models.Model):
    """ Comments objects """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    # connect to Post model
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
    text = models.TextField(blank=False)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    modified_at = models.DateTimeField(editable=False, blank=True, auto_now=True)  # auto_now => called everytime save() is called

    def __str__(self):
        return self.text[:25]
