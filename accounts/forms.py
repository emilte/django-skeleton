# imports
from django import forms
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm

from accounts.models import *
from accounts import models as account_models

User = get_user_model()

# End: imports -----------------------------------------------------------------

class SignUpForm(UserCreationForm):

    required_css_class = "required font-bold"
    code = forms.CharField(required=False, label="Kode")

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            # 'employee_nr',
            # 'nickname',
            # 'department',
            'phone_number',
            'gender',
        ]

    def __init__(self, *args, **kwargs):
        super(type(self), self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['password1'].help_text = "Your password can't be too similar to your other personal information. Your password must contain atleast 8 characters. Your password cant be a commonly used password and cant be entierly numeric."


class EditUserForm(forms.ModelForm):

    required_css_class = "required font-bold"

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'gender',
            # 'employee_nr',
            # 'nickname',
            # 'department',
        ]


    def __init__(self, *args, **kwargs):
        super(type(self), self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


# Possible to customise login:
class CustomAuthenticationForm(AuthenticationForm): # Not currently in use. Can be passed to login view
    error_messages = dict(AuthenticationForm.error_messages) # Inherit from parent. invalid_login and inactive

    # Override username to be compatible with employee_nr
    # username = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'autofocus': True}))

    def __init__(self, *args, **kwargs):
        super(type(self), self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class CustomPasswordChangeForm(PasswordChangeForm):
    # Inherited fields:
    # old_password
    # new_password1
    # new_password2

    class Meta:
        model = User
        exclude = []
        labels = {
            'old_password': 'Gammelt passord',
            'new_password1': 'Nytt passord',
            'new_password2': 'Nytt passord bekreftelse',
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        super(CustomPasswordChangeForm, self).__init__(request.user, *args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        # self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        # self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        # self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})
