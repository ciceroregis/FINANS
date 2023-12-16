from django.contrib import admin

from banks_accounts.models import Account_types, Accounts, Banks
from transactions.models import Category


# Register your models here.


@admin.register(Accounts)
class AccountsAdmin(admin.ModelAdmin):
    model = Accounts
    list_display = ('description', 'type', 'amount', 'bank', 'archived', 'main', 'created_at', 'updated_at', 'user')

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        user = request.user
        obj.user = user
        super(AccountsAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(AccountsAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


@admin.register(Account_types)
class AccountTypeAdmin(admin.ModelAdmin):
    model = Account_types
    list_display = ('name', 'description', 'created_at', 'updated_at')


@admin.register(Banks)
class BanksInlineForm(admin.ModelAdmin):
    model = Banks
    list_display = ('name', 'code', 'created_at', 'updated_at')


@admin.register(Category)
class CategoryInlineForm(admin.ModelAdmin):
    model = Category
    list_display = ['name']
