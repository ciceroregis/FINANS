from django.contrib.auth.models import User
from django.db import models


class Banks(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'

    name = models.CharField(max_length=250, verbose_name='Nome', null=False, blank=False)
    code = models.CharField(max_length=3, unique=True, blank=False, null=False, verbose_name='Código')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')

    def __str__(self):
        return self.name


class Account_types(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = 'Tipo de conta'
        verbose_name_plural = 'Tipos de conta'

    name = models.CharField(max_length=500, verbose_name='Nome', null=True, blank=False)
    description = models.TextField(max_length=500, null=True, blank=False, verbose_name='Descrição')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')

    def __str__(self):
        return self.name


class Accounts(models.Model):
    class Meta:
        ordering = ['bank']
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'

    amount = models.FloatField(blank=True, verbose_name='Saldo Bancário', default=0.0)
    archived = models.BooleanField(default=False, verbose_name='Arquivado')
    bank = models.ForeignKey(Banks, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='Banco')
    canceled = models.BooleanField(default=False, verbose_name='Cancelado')
    main = models.BooleanField(default=False, verbose_name='Conta Principal')
    description = models.CharField(max_length=200, null=True, blank=True, verbose_name='Descrição')
    type = models.ForeignKey(Account_types, on_delete=models.DO_NOTHING, verbose_name='Tipo da conta')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, verbose_name='Usuário')

    def __str__(self):
        return str(self.bank) + " - " + self.description.upper()
