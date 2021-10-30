# imports
import typing

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

User = get_user_model()

if typing.TYPE_CHECKING:
    from django.http import HttpRequest

# End: imports -----------------------------------------------------------------


class SignUpForm(UserCreationForm):

    required_css_class = 'required font-bold'
    code = forms.CharField(required=False, label='Kode')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'gender',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['password1'].help_text = "Your password can't be too similar to your other personal information. \
        Your password must contain at least 8 characters. \
        Your password can't be a commonly used password nor entierly numeric."


class EditUserForm(forms.ModelForm):

    required_css_class = 'required font-bold'

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'gender',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class CustomAuthenticationForm(AuthenticationForm):
    """ AuthenticationForm compatible with Bootstrap. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class CustomPasswordChangeForm(PasswordChangeForm):

    class Meta:
        model = User
        exclude = []
        labels = {
            'old_password': 'Gammelt passord',
            'new_password1': 'Nytt passord',
            'new_password2': 'Nytt passord bekreftelse',
        }

    def __init__(self, *args, **kwargs):
        request: HttpRequest = kwargs.pop('request')
        super().__init__(request.user, *args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
