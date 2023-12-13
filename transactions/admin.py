from django.contrib import admin

from transactions.models import Transactions


@admin.register(Transactions)
class TransactionsInlineForm(admin.ModelAdmin):
    model = Transactions
    list_display = ('description', 'accounts', 'account_type', 'category', 'value', 'recurring', 'note',
                    'total_installments',
                    'date_transaction',
                    'attachments',
                    'paid',
                    'type',
                    'date_transaction',
                    'created_at',
                    'updated_at', 'user')
    list_per_page = 5

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        user = request.user
        obj.user = user
        super(TransactionsInlineForm, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(TransactionsInlineForm, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
