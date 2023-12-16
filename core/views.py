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


@login_required
def home(request):
    context = {
        "bank_account_list": bank_account_list(request),
    }
    return render(request, 'home.html', context)
