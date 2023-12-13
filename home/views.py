from collections import Counter

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum, Q
from django.views.decorators.http import require_GET
from django.shortcuts import render

from banks_accounts.models import Accounts
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

    paginator = Paginator(accounts, 10)
    page = request.GET.get('page', 1)
    try:
        accounts = paginator.get_page(page)
    except PageNotAnInteger:
        accounts = paginator.get_page(1)
    except EmptyPage:
        accounts = paginator.get_page(paginator.num_pages)
    return accounts


@require_GET
def incomes_card(request):
    incomes = Transactions.objects.filter(
        type__icontains='Receitas', user=request.user).aggregate(total=Sum('value'))
    if incomes['total'] is None:
        return None
    return incomes


@require_GET
def expenses_card(request):
    expenses = Transactions.objects.filter(
        type__icontains='Despesas', user=request.user).aggregate(total=Sum('value'))
    if expenses['total'] is None:
        return None
    return expenses


@require_GET
def monthly_balance(request):
    incomes = Counter(incomes_card(request))
    expenses = Counter(expenses_card(request))
    if incomes['total'] is None or expenses['total'] is None:
        return None
    balance = incomes['total'] - expenses['total']
    if balance:
        return balance


@login_required
def home(request):
    context = {
        "total_incomes": incomes_card(request),
        "total_expenses": expenses_card(request),
        "monthly_balance": monthly_balance(request),
        "bank_account_list": bank_account_list(request),

    }
    return render(request, 'home.html', context)
