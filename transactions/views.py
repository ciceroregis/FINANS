from collections import Counter

from django.db.models import Q
from django.http import HttpResponseNotAllowed, HttpResponseNotFound
import decimal
import logging
from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.db.models import Sum, Q

from transactions.form import TransactionForm
from transactions.models import Accounts, Transactions
from utils.push_notification import notifications
from utils.installments import calculate_installments


@login_required
@require_GET
def incomes_card(request):
    incomes = Transactions.objects.filter(
        type__icontains='Receitas', user=request.user).aggregate(total=Sum('value'))
    if incomes['total'] is None:
        return None
    return incomes


@login_required
@require_GET
def expenses_card(request):
    expenses = Transactions.objects.filter(
        type__icontains='Despesas', user=request.user).aggregate(total=Sum('value'))
    if expenses['total'] is None:
        return None
    return expenses


@login_required
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
@require_GET
def list_transactions(request):
    today = date.today()  # a data atual como uma variável de contexto para o modelo
    search = request.GET.get("search")
    transactions = _get_transactions(request.user, search)
    pending_transactions = [trans for trans in transactions if not trans.paid and trans.date_transaction <= today]
    request.session['pending_transactions'] = [trans.description for trans in pending_transactions]
    paginator = Paginator(transactions, 10)
    page = request.GET.get("page", 1)
    transactions = paginator.get_page(page)
    context = {
        'list_transactions': transactions,
        'today': today,
        'pending_transactions': pending_transactions,
        'notifications': notifications(request),
        'incomes': incomes_card(request),
        'expenses': expenses_card(request),
        'balance': monthly_balance(request)
    }
    return render(request, "list_transactions.html", context)


def _get_transactions(user, search):
    if search:
        return Transactions.objects.filter(
            Q(user=user, description__icontains=search) |
            Q(user=user, accounts__bank__name__icontains=search) |
            Q(user=user, value__icontains=search) |
            Q(user=user, paid__icontains=search)
        )
    else:
        return Transactions.objects.filter(user=user).all().order_by("description")


@login_required
def create_transaction(request):
    form = TransactionForm(user=request.user)

    if request.method == "POST":
        form = TransactionForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            try:
                transaction = form.save(commit=False)
                transaction.user = request.user
                value = form.cleaned_data.get('value')
                transaction.value = decimal.Decimal(value.replace(",", ""))
                transaction.attachments = form.cleaned_data.get('attachments')
                transaction.save()
                messages.success(request, "Lançamento adicionado com sucesso! ")
                return redirect("list_transactions")
            except Exception as e:
                messages.warning(request, "Ocorreu um erro ao salvar o Lançamento")
                logging.exception(e)
                return redirect("create_transaction")
    context = {"form": form}
    return render(request, "create_transaction.html", context)


@login_required
@require_GET
def transaction_details(request, pk):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    try:
        transaction = Transactions.objects.get(id=pk, user=request.user)
    except Transactions.DoesNotExist:
        return HttpResponseNotFound()
    details = Transactions.objects.filter(id=pk, user=request.user)
    installments = calculate_installments(value=transaction.value, total=transaction.total_installments)
    context = {
        'details': details,
        'installments': installments,
        'installment_value': installments.get('installment_value', 0),
    }
    return render(request, "transaction_details.html", context)


@login_required
def update_transaction(request, pk):
    title = {}
    if pk:
        title = "Editar Lançamento"
    try:
        transaction = Transactions.objects.get(id=pk, user=request.user)
    except Transactions.DoesNotExist:
        messages.warning(request, "O Lançamento não existe.")
        return redirect("list_transactions")

    if request.method == "POST":
        form = TransactionForm(request.POST, request.FILES,
                               instance=transaction, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            value = form.cleaned_data.get('value')
            transaction.value = decimal.Decimal(value.replace(",", ""))
            transaction.attachments = form.cleaned_data.get('attachments')
            transaction.select = form.cleaned_data.get('select')
            transaction.save()
            messages.success(request, "Lançamento atualizado com sucesso!")
            return redirect("/transactions_details/{0}".format(transaction.pk), messages)
        else:
            messages.error(request, "Ocorreu um erro ao tentar salvar o fomulário")
            context = {"form": form, }
    else:
        form = TransactionForm(instance=transaction, user=request.user)
        context = {
            "form": form,
            "title": title
        }
    return render(request, "create_transaction.html", context)


@login_required
def remove_transaction(request, pk):
    if request.method == 'POST':
        confirm = request.POST.get('confirm')
        if confirm == 'yes':
            try:
                transaction = Transactions.objects.get(pk=pk)
                transaction.delete()
                messages.success(request, 'Lançamento removido com sucesso.')
                return redirect('list_transactions')
            except Accounts.DoesNotExist:
                messages.error(request, 'Lançamento não encontrado.')
                return redirect('list_transactions')
        else:
            messages.warning(request, 'Ação cancelada.')
            return redirect('list_transactions')
    else:
        return render(request, 'remove_transaction.html', {'transaction_id': pk})


@login_required
def mark_account_as_paid(request, pk):
    try:
        account = Transactions.objects.get(id=pk, user=request.user)
    except Transactions.DoesNotExist:
        messages.warning(request, "Lançamento não existe ou já está pago.")
        return redirect("list_transactions")
    if account.paid is False:
        account.paid = True
        account.date_transaction = datetime.now().date()
        account.save()
        messages.success(request, f"Lançamento  pago com sucesso!")
    else:
        messages.warning(request, "Ação não permitida.")
    return redirect("list_transactions")
