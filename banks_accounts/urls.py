from django.urls import path

from banks_accounts import views

urlpatterns = [
    # Accounts Bank
    path('banks_accounts_details/<str:pk>', views.account_details, name='banks_accounts_details'),
    path('banks_accounts/<str:pk>/archive_bank_account', views.archive_account, name='archive_bank_account'),
    path('create_bank_account', views.create_bank_account, name='create_bank_account'),
    path("update_banks_accounts/<str:pk>", views.update_account, name="update_bank_account"),
    path("remove_bank_account/<str:pk>", views.remove_bank_account, name="remove_bank_account"),

]
