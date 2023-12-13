from django.urls import path
from dashboard import views

urlpatterns = [
    path('charts/', views.transactions_charts, name='charts'),
]

