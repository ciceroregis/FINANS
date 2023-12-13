
import datetime


def calculate_installments(value, total):
    """Calcula as parcelas de um valor total.

    Args:
        value: O valor total a ser parcelado.
        total: O número total de parcelas.

    Returns: Um dicionário com as informações sobre as parcelas. Se houver algum erro, retorna um dicionário com a
    chave 'error'.

    Raises:
        ValueError: Se o valor total for negativo.
        TypeError: Se o valor total não for numérico.
    """
    if total is None or total <= 0:
        return {'noInstallments': 'Não possui parcelas.'}

    try:
        total_value = float(value)
    except (ValueError, TypeError):
        return {'error': 'Valor inválido.'}

    try:
        installment_value = round(total_value / total, 2)
    except ZeroDivisionError:
        return {'error': 'Número de parcelas inválido.'}

    installments = [f'{i + 1}/{total}' for i in range(total)]

    # Calcula o número de meses desde o início do pagamento
    start_date = datetime.date.today()
    months_since_start = ((
        datetime.date.today().year - datetime.date.today().month) - (datetime.date.today().year - start_date.month)
    ) * 12 + (datetime.date.today().month - start_date.month)

    # Calcula o valor da parcela atual com base no número de meses desde o início do pagamento
    current_installment = months_since_start + 1

    return {
        'installments': installments[current_installment - 1],
        'installment_value': installment_value,
    }
