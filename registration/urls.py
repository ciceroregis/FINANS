from django.contrib.auth.views import LogoutView

from django.contrib.auth import views as auth_views
from django.urls import path
from core import settings

from registration.views import register_user,show_user_profile,update_profile_data,password_reset_request

urlpatterns = [
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path('register/', register_user, name="register"),
    path('user_profile/', show_user_profile, name="user_profile"),
    path('update_profile/<str:pk>', update_profile_data, name="update_profile"),
    path("password_reset/", password_reset_request, name="password_reset"),
    path("logout/", LogoutView.as_view(),{'next_page': settings.LOGOUT_REDIRECT_URL}, name="logout")
]
