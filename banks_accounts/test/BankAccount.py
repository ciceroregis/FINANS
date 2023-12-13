from django.utils import timezone
from django.test import Client, TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse

from banks_accounts.models import Accounts, Account_types, Banks
from home.views import incomes_card
from transactions.models import Transactions


class BankAccountListTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.account_type = Account_types.objects.create(name='Checking')
        self.income_type = Transactions.objects.create(type='Receitas', user=self.user, date_transaction=timezone.now())
        self.expense_type = Transactions.objects.create(type='Despesas', user=self.user,
                                                        date_transaction=timezone.now())

        self.bank = Banks.objects.create(name='Bank A')
        self.factory = RequestFactory()

    def test_bank_account_list_view_with_login(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_bank_account_list_view_without_login(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/?next='))

    def test_bank_account_list_view_with_search(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('home'), {'search': 'test bank'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        accounts = response.context['bank_account_list']
        self.assertTrue(all(account.bank.name.lower().find('test bank') != -1 for account in accounts))

    def test_bank_account_list_view_pagination(self):
        self.client.login(username='testuser', password='password')
        for i in range(20):
            Accounts.objects.create(description='Test Bank {}'.format(i), user=self.user, type=self.account_type)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        accounts = response.context['bank_account_list']
        self.assertEqual(len(accounts), 10)

    def test_incomes_card_with_no_data(self):
        request = self.factory.get('/incomes_card/')
        request.user = self.user
        response = incomes_card(request)
        self.assertIsInstance(response, dict)
        self.assertIn('total', response)
        self.assertEqual(response['total'], 0.0)

    def test_incomes_card_with_data(self):
        Transactions.objects.create(value=100, user=self.user, type='Receitas', date_transaction=timezone.now())
        Transactions.objects.create(value=200, user=self.user, type='Receitas', date_transaction=timezone.now())
        request = self.factory.get('/incomes_card/')
        request.user = self.user
        response = incomes_card(request)
        self.assertEqual(response['total'], 300)

