# imports
import typing

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import Group

if typing.TYPE_CHECKING:
    pass
# End: imports -----------------------------------------------------------------


class User(auth_models.User):

    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        OTHER = 'O', 'Other'

    # department = models.ForeignKey('accounts.Department', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Avdeling', related_name='users')
    # nickname = models.CharField(max_length=150, unique=True, null=True, blank=False, verbose_name='Kallenavn')
    gender = models.CharField(max_length=1, choices=Gender.choices, default=None, null=True, blank=True, verbose_name='Kjønn')
    phone_number = models.CharField(max_length=13, default=None, null=True, blank=True, verbose_name='Mobilnummer')

    class Meta:
        ordering = ['username']

    def __str__(self):
        return f'{self.get_full_name() or self.username or self.email or self.id}'


class PermissionCode(models.Model):
    """ Secret code that users can submit to join groups. """
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, blank=False)
    secret = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return f'PermissionCode ({self.group}:{self.secret})'


class Department(models.Model):
    """
    Like Group, but with no permissions.

    Can be used for visual affiliations.
    Supports hierarchical departments.
    """
    name = models.CharField(max_length=200, null=False, blank=False, verbose_name='Navn')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', verbose_name='Over-seksjon')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='accounts.DepartmentMembership', related_name='departments', verbose_name='Medlemmer')

    class Meta:
        ordering = []
        verbose_name = 'Seksjon'
        verbose_name_plural = 'Seksjoner'

    def __str__(self):
        return f'{self.name}'

    def root_path(self, path=None):
        path = path or []
        path.append(self)
        if self.parent:
            return self.parent.root_path(path)
        return path

    def member_count(self):
        return self.members.all().count()


class DepartmentMembership(models.Model):
    """ Intermediate model: User <-> Department """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False, verbose_name='Bruker')
    department = models.ForeignKey('accounts.Department', on_delete=models.CASCADE, null=False, blank=False, verbose_name='Seksjon')
    date_joined = models.DateTimeField(default=timezone.now, null=False, blank=False, verbose_name='Dato innmeldt')

    class Meta:
        ordering = ['id']
        verbose_name = 'Medlem'
        verbose_name_plural = 'Medlemmer'

    def __str__(self):
        return f'Medlem: {self.user}'
