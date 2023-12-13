from django import forms
from transactions.models import Accounts, Category, Transactions


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transactions
        exclude = (
            "created_at",
            "updated_at",
        )

    description = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control", "placeholder": "Informa descrição da conta",
            }
        ),
        required=False,
    )

    value = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control ",
                   "placeholder": "Informe o valor da conta",
                   "onkeypress": "$(this).mask('#,##0.00', {reverse: true})"}),
        required=False,
    )

    category = forms.ModelChoiceField(
        widget=forms.Select(
            attrs={"class": "form-control", "data-placeholder": "Informe a categoria"}
        ),
        queryset=Category.objects.all(),
        required=False,
    )

    date_transaction = forms.DateField(
        widget=forms.DateInput(

            attrs={
                "class": "form-control",
                'style': 'display:inline;',
                "id": "datetimepicker",
                "autocomplete": "off",
                "placeholder": "Data do Lançamento",
            }
        ),
        required=False,
    )
    paid = forms.CharField(
        widget=forms.CheckboxInput(
            attrs={'class': "checkbox form-check-input", "placeholder": "pago"}
        ),
    )

    recurring = forms.CharField(
        widget=forms.CheckboxInput(
            attrs={'class': "checkbox form-check-input", "id": "checkbox", "placeholder": "Repete"}
        ),
    )

    select = forms.ChoiceField(
        widget=forms.Select(attrs={
            'style': 'display:none; margin-left:-10px',
            'id': 'select',
            'class': 'form-control'
        }),
        required=False,
        label=True,
        choices=Transactions.FREQUENCIES
    )
    total_installments = forms.IntegerField(
        widget=forms.TextInput(attrs={
            'style': 'display:none; '
                     'margin-left:-10px',
            'id': 'total_installments',
            'class': 'form-control',
            "placeholder": "Parcelas"
        }),
        required=False,
        label=True,
    )

    type = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label=True,
        required=False,
        choices=Transactions.TYPE_CHOICES
    )

    note = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control", "placeholder": "Observação",
            }
        ),
        required=False,
    )

    attachments = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "type": "file", "class": "form-control"
            },
        ),
        required=False,
    )

    accounts = forms.ModelChoiceField(
        widget=forms.Select(
            attrs={"class": "form-control", "data-placeholder": "Informe a conta"}
        ),
        queryset=Accounts.objects.none(),
        required=True
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['accounts'].queryset = Accounts.objects.filter(user=user)
        self.fields['recurring'].widget.attrs.update({'id': 'checkbox'})
        self.fields['attachments'].widget.attrs.update({'accept': '*', 'data-target': "_blank"})
        self.fields['accounts'].queryset = Accounts.objects.filter(user=user)

    def clean(self, *args, **kwargs):
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        value = cleaned.get('value')
        date_transaction = cleaned.get('date_transaction')
        category = cleaned.get('category')
        description = cleaned.get('description')
        type = cleaned.get('type')

        error_msg_required_field = 'Este campo é obrigatório.'

        if not value:
            validation_error_msgs['value'] = error_msg_required_field

        if not date_transaction:
            validation_error_msgs['date_transaction'] = error_msg_required_field

        if not category:
            validation_error_msgs['category'] = error_msg_required_field

        if not description:
            validation_error_msgs['description'] = error_msg_required_field

        if not type:
            validation_error_msgs['type'] = error_msg_required_field

        if validation_error_msgs:
            raise (forms.ValidationError(validation_error_msgs))
