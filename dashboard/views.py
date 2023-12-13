from django.db.models import Sum
from django.shortcuts import render

from transactions.models import Transactions
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required


@require_GET
@login_required
def transactions_charts(request):
    def get_incomes_by_category(user):
        return Transactions.objects.filter(type='Receitas', user=user).\
            values('category__name').annotate(total=Sum('value')).order_by('category')

    def get_expenses_by_category(user):
        return Transactions.objects.filter(type='Despesas', user=user) \
            .values('category__name').annotate(total=Sum('value')).order_by('category')

    incomes_by_category = get_incomes_by_category(request.user)
    expenses_by_category = get_expenses_by_category(request.user)

    total_income = incomes_by_category.aggregate(total=Sum('value')).get('total', 0)
    total_expense = expenses_by_category.aggregate(total=Sum('value')).get('total', 0)

    incomes_with_percentage = [{
        'category_name': income['category__name'],
        'total': income['total'],
        'percentage': (income['total'] / total_income) * 100
    } for income in incomes_by_category]

    expenses_with_percentage = [{
        'category_name': expense['category__name'],
        'total': expense['total'],
        'percentage': (expense['total'] / total_expense) * 100
    } for expense in expenses_by_category]

    context = {
        'incomes_with_percentage': incomes_with_percentage,
        'expenses_with_percentage': expenses_with_percentage,
    }
    return render(request, 'charts.html', context)
