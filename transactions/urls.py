from django.urls import path

from transactions import views

urlpatterns = [

    # Transactions
    path("list_transactions/", views.list_transactions, name="list_transactions"),
    path('create_transaction', views.create_transaction, name='create_transaction'),
    path('transactions_details/<str:pk>', views.transaction_details, name='transactions_details'),
    path("update_transaction/<str:pk>", views.update_transaction, name="update_transaction"),
    path("remove_transaction/<str:pk>", views.remove_transaction, name="remove_transaction"),
    path("list_transactions/<str:pk>", views.mark_account_as_paid, name="mark_account_as_paid"),

]
