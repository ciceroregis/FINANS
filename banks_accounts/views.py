import decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.http import require_GET

from banks_accounts.form import AccountForm
from banks_accounts.models import Accounts
from transactions.models import Transactions


@login_required
def create_bank_account(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            try:
                bank_account = form.save(commit=False)
                bank_account.user = request.user
                amount = form.cleaned_data.get('amount')
                bank_account.amount = decimal.Decimal(amount.replace(",", ""))
                bank_account.save()
                messages.success(request, "A conta bancária foi criada com sucesso! ")
                return redirect("home")
            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao cadastrar a conta bancária: {e}")
    else:
        form = AccountForm()
    context = {
        "form": form,
    }
    return render(request, "banks_accounts/create_bank_account.html", context)


@login_required
@require_GET
def account_details(request, pk):
    context = {}
    try:
        accounts = Accounts.objects.get(id=pk)
        expenses = Transactions.objects.filter(type=Transactions.EXPENSES, accounts_id=pk)
        incomes = Transactions.objects.filter(type=Transactions.INCOMES, accounts_id=pk)
        context = {
            'account': accounts,
            'num_expenses': expenses.count(),
            'num_incomes': incomes.count()
        }
    except Accounts.DoesNotExist:
        messages.warning(request, 'A conta não foi encontrada')
    except Transactions.DoesNotExist:
        messages.warning(request, 'Não foram encontradas transações para essa conta')
    return render(request, "banks_accounts/account_details.html", context)


@login_required
@require_GET
def archive_account(request, pk):
    try:
        account = Accounts.objects.get(id=pk)
    except Accounts.DoesNotExist:
        messages.error(request, "Conta bancária não encontrada.")
        return redirect('home')

    if account.archived:
        account.archived = False
        messages.success(request, "Conta bancária desarquivada com sucesso.")
    else:
        account.archived = True
        messages.success(request, "Conta bancária arquivada com sucesso.")

    account.save()
    return redirect("banks_accounts_details", pk=account.pk)


@login_required
def update_account(request, pk):
    title = "Editar Conta" if pk else {}
    try:
        bank_account = Accounts.objects.get(id=pk)
    except Accounts.DoesNotExist:
        messages.error(request, "Conta bancária não encontrada.")
        return redirect('home')

    if request.method == "POST":
        form = AccountForm(request.POST, instance=bank_account)
        if form.is_valid():
            bank_account = form.save(commit=False)
            bank_account.user = request.user
            amount = form.cleaned_data.get('amount').replace(",", "")
            bank_account.amount = decimal.Decimal(amount)
            bank_account.save()
            messages.success(request, "Conta bancária atualizada com sucesso.")
            return redirect("banks_accounts_details", pk=bank_account.pk)
        else:
            messages.warning(request, "Por favor, corrija o erro abaixo.")
    else:
        form = AccountForm(instance=bank_account)

    context = {"form": form, "title": title}
    return render(request, "banks_accounts/create_bank_account.html", context)


@login_required
def remove_bank_account(request, pk):
    if request.method == 'POST':
        confirm = request.POST.get('confirm')
        if confirm == 'yes':
            try:
                account = Accounts.objects.get(pk=pk)
                account.delete()
                messages.success(request, 'Conta bancária removida com sucesso.')
                return redirect('home')
            except Accounts.DoesNotExist:
                messages.error(request, 'Conta bancária não encontrada.')
                return redirect('home')
        else:
            messages.info(request, 'Ação cancelada.')
            return redirect('home')
    else:
        return render(request, 'banks_accounts/remove_bank_account.html', {'account_id': pk})


