import os
from django.contrib.auth.models import User
from django.db import models

from banks_accounts.models import Accounts, Account_types


class Category(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    name = models.CharField(max_length=200, null=True, blank=True, verbose_name='Categoria')

    def __str__(self):
        return self.name


class Transactions(models.Model):
    INCOMES = 'Receitas'
    EXPENSES = 'Despesas'

    TYPE_CHOICES = [
        ('', '---------'),
        (INCOMES, 'Receitas'),
        (EXPENSES, 'Despesas'),
    ]

    FREQUENCIES = [
        ('', '---------'),
        ('Diariamente', 'Diariamente'),
        ('Semanalmente', 'Semanalmente'),
        ('Mensalmente', 'Mensalmente'),
        ('Anualmente', 'Anualmente'),
    ]

    class Meta:
        ordering = ['description']
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'

    accounts = models.ForeignKey(Accounts, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Conta')
    account_type = models.ForeignKey(Account_types,
                                     on_delete=models.CASCADE, null=True, blank=True, verbose_name='Tipo de conta')
    attachments = models.FileField(upload_to="attachments/",
                                   max_length=200, null=True, blank=True, verbose_name='Anexos')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Categoria')
    date_transaction = models.DateField(auto_created=False, verbose_name='Data da Transação')
    description = models.CharField(max_length=200, null=True, blank=True, verbose_name='Descrição')
    note = models.CharField(max_length=500, verbose_name='Observação')
    paid = models.BooleanField(default=False, verbose_name='Pago')
    recurring = models.BooleanField(default=False, verbose_name='Repete')
    select = models.CharField(max_length=12,
                              default='', blank=False, null=False, choices=FREQUENCIES, verbose_name='Frequência')
    paid_installment = models.PositiveIntegerField(null=True, blank=True, verbose_name='Parcela paga')
    total_installments = models.IntegerField(null=True, blank=True, verbose_name='Parcelas Totais')
    type = models.CharField(max_length=10,
                            default='', blank=False, null=False, choices=TYPE_CHOICES, verbose_name='Despesas e Receita')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, verbose_name='Usuário')
    value = models.CharField(max_length=200, null=False, blank=True, verbose_name='Valor')

    def __str__(self):
        if self.description is not None:
            return str(self.accounts) + " - " + self.description.upper()
        else:
            return str(self.accounts)

    @property
    def filename(self):
        return os.path.basename(self.attachments.name)
