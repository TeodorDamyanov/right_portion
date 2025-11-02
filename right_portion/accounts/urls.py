from django.urls import path, include
from right_portion.accounts.views import *

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name="register user"),
    path("login/", UserLoginView.as_view(), name="login user"),
    path("logout/", UserLogoutView.as_view(), name="logout user"),
    path("profile/<int:pk>/", include([
        path("", UserDetailsView.as_view(), name="profile details"),
        path("edit/", UserEditView.as_view(), name='profile edit'),
        path("delete/", UserDeleteView.as_view(), name='profile delete')
    ]))
]