from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum, Q, F
from django.views.decorators.http import require_GET
from django.shortcuts import render

from banks_accounts.models import Accounts
from transactions import models
from transactions.models import Transactions


@login_required
@require_GET
def bank_account_list(request):
    search = request.GET.get('search')
    accounts = Accounts.objects.filter(user=request.user).order_by('description')
    if search:
        accounts = accounts.filter(
            Q(bank__code__icontains=search) |
            Q(bank__name__icontains=search) |
            Q(description__icontains=search)
        )
    else:
        accounts = accounts.order_by('bank')
    return accounts


@login_required
def calculate_individual_account_balances(request):
    user_accounts = Accounts.objects.filter(user=request.user)

    account_balances = []

    for account in user_accounts:
        transactions_sum = (
            Transactions.objects
            .filter(accounts=account)
            .aggregate(expenses=Sum('value', filter=Q(type=Transactions.EXPENSES)),
                       income=Sum('value', filter=Q(type=Transactions.INCOMES)))
        )
        expenses = transactions_sum.get('expenses') or 0
        income = transactions_sum.get('income') or 0

        account_balance = (float(account.amount) if account.amount else 0) - expenses + income
        account_balances.append({'account': account.description, 'balance': account_balance})

    return account_balances


@login_required
def get_total_account_balance(request):
    account_balances = calculate_individual_account_balances(request)
    total_balance = sum(balance['balance'] for balance in account_balances)
    return total_balance


@login_required
def home(request):
    context = {
        "bank_account_list": bank_account_list(request),
        "get_total_account_balance": get_total_account_balance(request),
        "calculate_individual_account_balances": calculate_individual_account_balances(request)
    }
    return render(request, 'home.html', context)
