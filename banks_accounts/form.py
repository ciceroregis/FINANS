import requests
from django import forms
from banks_accounts.models import Account_types, Accounts, Banks
from django_select2.forms import Select2Widget


class AccountForm(forms.ModelForm):
    class Meta:
        model = Accounts
        exclude = (
            "created_at",
            "updated_at",
        )

    bank = forms.ModelChoiceField(
        widget=Select2Widget(attrs={"class": "form-control select2",
                                    "id": "datalistOptions",
                                    "data-placeholder": "Informe o nome do banco"}),

        queryset=Banks.objects.all(),
        required=False,
    )

    description = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control", "placeholder": "Informa descrição da conta",
            }
        ),
        required=False,
    )

    amount = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control ",
                                      "placeholder": "Informa o valor inicial da conta",
                                      "onkeypress": "$(this).mask('#,##0.00', {reverse: true})"}),
        required=False,
    )

    type = forms.ModelChoiceField(
        widget=forms.Select(
            attrs={"class": "form-control", "data-placeholder": "Informe o tipo da conta"}
        ),
        queryset=Account_types.objects.all(),
        required=False,
    )

    main = forms.CharField(
        widget=forms.CheckboxInput(
            attrs={'class': "checkbox form-check-input", "placeholder": "Conta principal"}
        ),
    )

    def clean(self, *args, **kwargs):
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        bank = cleaned.get('bank')
        description = cleaned.get('description')
        type_account = cleaned.get('type')
        amount = cleaned.get('amount')

        error_msg_required_field = 'Este campo é obrigatório.'

        if not description:
            validation_error_msgs['description'] = error_msg_required_field

        if not bank:
            validation_error_msgs['bank'] = error_msg_required_field

        if not type_account:
            validation_error_msgs['type'] = error_msg_required_field

        if not amount:
            validation_error_msgs['amount'] = error_msg_required_field

        if validation_error_msgs:
            raise (forms.ValidationError(validation_error_msgs))

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # obter dados da API
    #     url = 'https://brasilapi.com.br/api/banks/v1'
    #     response = requests.get(url)
    #     data = response.json()
    #
    #     data = filter(lambda banco: banco['code'] is not None, data)
    #     for banco in data:
    #         name = banco['name']
    #         code = banco['code']
    #         self.instance = Banks(name=name, code=code)
    #         print(self.instance)
    #         self.instance.save()
