from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

from registration.views import password_reset_request
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("banks_accounts.urls")),
    path('', include("registration.urls")),
    path('', include("transactions.urls")),
    path('', include('dashboard.urls')),
    path('', views.home, name='home'),



    path('change_password/', auth_views.PasswordChangeView.as_view(
        template_name='registration/change_password.html', success_url='/password_change_done/'),
         name='change_password'),
    path('forgot_password/', auth_views.PasswordChangeView.as_view(
        template_name='registration/forgot-password.html', success_url='/password_change_done/'),
         name='change_password'),
    path("password_reset", password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password/password_reset_complete.html'), name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
