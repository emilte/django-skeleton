# imports
import json

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import Avg, Count, Min, Sum
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


# End: imports -----------------------------------------------------------------

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password=None, **kwargs):
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **kwargs):
        user = self.create_user(username=username, password=password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"
    GENDER_CHOICES = [
        (None, None),
        (MALE, "Mann"),
        (FEMALE, "Kvinne"),
        (OTHER, "Annet"),
    ]
    username = models.CharField(max_length=60, unique=True, verbose_name="brukernavn")
    email = models.EmailField(max_length=254, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=60, null=True, blank=True, verbose_name="Fornavn")
    last_name = models.CharField(max_length=150, null=True, blank=True, verbose_name="Etternavn")
    # department = models.ForeignKey('accounts.Department', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Avdeling", related_name="users")
    # nickname = models.CharField(max_length=150, unique=True, null=True, blank=False, verbose_name="Kallenavn")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=None, null=True, blank=True, verbose_name="Kjønn")
    is_active = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=13, default=None, null=True, blank=True, verbose_name="Mobilnummer")
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now, blank=True, editable=False, verbose_name="Opprettet")

    objects = auth_models.UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['username']

    def __str__(self):
        return f"{self.get_full_name() or self.username or self.email or self.id}"

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return None

    def get_username(self):
        return self.username

    def get_short_name(self):
        return self.first_name


    def serialize(self):
        jayson = {}
        jayson['id'] = self.id
        # jayson['email'] = self.email
        jayson['nickname'] = self.nickname
        jayson['first_name'] = self.first_name
        jayson['last_name'] = self.last_name
        jayson['department'] = self.department
        jayson['is_staff'] = self.is_staff
        jayson['is_superuser'] = self.is_superuser
        return jayson


class PermissionCode(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, blank=False)
    secret = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return f"PermissionCode ({self.group}:{self.secret})"



class Department(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name="Tittel")
    parent = models.ForeignKey('accounts.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name="children", verbose_name="Over-seksjon")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='accounts.Member', blank=True, related_name="departments", verbose_name="Medlemmer")

    class Meta:
        ordering = []
        verbose_name = "Seksjon"
        verbose_name_plural = "Seksjoner"

    def __str__(self):
        return f"{self.title}"

    def root_path(self, path=[]):
        path.append(self)
        if self.parent:
            return self.parent.root_path(path)
        return path

    def member_count(self):
        return self.members.all().count()

# Intermediate model
class Member(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Bruker")
    department = models.ForeignKey('accounts.Department', on_delete=models.CASCADE, null=False, blank=False, verbose_name="Event")
    date_joined = models.DateTimeField(default=timezone.now, null=False, blank=False, verbose_name="Dato påmeldt")
    # is_earlybird = models.BooleanField(default=False, verbose_name="Earlybird")
    # has_paid = models.BooleanField(default=False, verbose_name="Har betalt")

    class Meta:
        ordering = ['id']
        verbose_name = "Medlem"
        verbose_name_plural = "Medlemmer"

    def __str__(self):
        return f"Medlem: {self.user}"
