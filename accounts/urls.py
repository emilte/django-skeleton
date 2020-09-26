# imports
from django.urls import path
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views


from accounts import views
from accounts import forms as account_forms
# End: imports -----------------------------------------------------------------

app_name = 'accounts' # Necessary for url naming. eg {% url 'accounts:signin' %}

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    # path('login/', views.LoginView.as_view(), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name="accounts/login2.html", form_class=account_forms.CustomAuthenticationForm), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit_profile'),
    path('users/xlsx/', views.UsersXLSX.as_view(), name='users_xlsx'),

    #path('delete_user/', views.DeleteUserView.as_view(), name="delete_user"),



]
