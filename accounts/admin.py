# imports
import typing

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.models import Permission

from root import models as root_models
from accounts import models as account_models

if typing.TYPE_CHECKING:
    from django.http import HttpRequest
    from django.db.models import QuerySet

# End: imports -----------------------------------------------------------------

User = get_user_model()

# pylint: disable=unused-argument


# Actions for Admin-site:
@admin.action(description='Mark selected users as normal users without any permissions')
def make_normal_user(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(is_staff=False)
    queryset.update(is_superuser=False)


@admin.action(description='Mark selected users as is_staff')
def make_staff_user(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(is_staff=True)
    queryset.update(is_superuser=False)


@admin.action(description='Mark selected users as is_superuser')
def make_superuser(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(is_staff=True)
    queryset.update(is_superuser=True)


# End: Actions for Admin-site ---------------------------------------------------


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    list_display = ['username', 'id', 'email', 'first_name', 'last_name', 'gender', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'gender']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['last_name']
    readonly_fields = ['last_login', 'date_joined']
    filter_horizontal = ['groups', 'user_permissions']
    actions = [make_normal_user, make_staff_user, make_superuser]


@admin.register(account_models.PermissionCode)
class PermissionCodeAdmin(root_models.CustomBaseAdmin):
    list_display = ['group', 'secret']
    list_filter = ['group']
    search_fields = ['group', 'secret']
    ordering = ['-id']
    # readonly_fields = []
    # filter_horizontal = []
    # actions = []


@admin.register(account_models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'member_count']
    list_filter = ['parent']
    search_fields = ['name']
    # ordering = []
    # readonly_fields = []
    # filter_horizontal = []
    # actions = []


admin.site.register(Permission)
