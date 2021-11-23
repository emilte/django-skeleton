# imports
from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from accounts import forms as account_forms
from accounts import models as account_models

User = get_user_model()

# End: imports -----------------------------------------------------------------


@method_decorator([login_required], name='dispatch')
class ProfileView(View):
    template = 'accounts/profile.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template, {})


@method_decorator([login_required], name='dispatch')
class EditProfileView(View):
    template = 'accounts/edit_profile.html'
    form_class = account_forms.EditUserForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)
        return render(request, self.template, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profilen din har blitt oppdatert')
            return redirect('accounts:profile')
        return render(request, self.template, {'form': form})


class SignUpView(View):
    template = 'accounts/registration_form.html'
    form_class = account_forms.SignUpForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            try:
                code = form.cleaned_data['code']
                group = account_models.PermissionCode.objects.get(secret=code).group
                user.groups.add(group)
                messages.success(request, f'Med koden "{code}" har du blitt lagt til i avdeling: {group.name}')
            except:  # pylint: disable=bare-except
                messages.warning(request, f'Koden "{code}" tilsvarer ingen avdeling. Ta kontakt med admin')

            return redirect('home')
        return render(request, self.template, {'form': form})


@method_decorator([login_required], name='dispatch')
class DeleteUserView(View):

    def delete(self, request, *args, **kwargs):
        request.user.delete()
        logout(request)
        messages.success(request, 'Brukeren din har blitt slettet fra systemet')
        return redirect('home')


class LoginView(View):
    template = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template)

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        error = None
        if user is not None:
            login(request, user)
            return redirect('accounts:profile')
        error = 'Feil'

        return render(request, self.template, {'error': error})


@method_decorator([login_required], name='dispatch')
class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:login')


@method_decorator([login_required], name='dispatch')
class ChangePasswordView(View):
    template = 'accounts/change_password.html'
    form_class = account_forms.CustomPasswordChangeForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(request=request)
        return render(request, self.template, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, request=request)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('accounts:profile')
        return render(request, self.template, {'form': form})
