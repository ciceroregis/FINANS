from datetime import date

from notifications.models import Notification
from notifications.signals import notify

from transactions.models import Transactions


def get_unread_notifications_user(user):
    unread_notifications = Notification.objects.unread().filter(recipient=user)
    return unread_notifications


def count_notifications_unread_user(user):
    unread_notifications = get_unread_notifications_user(user).count()
    return unread_notifications


def send_pending_accounts_notification(user):
    today = date.today()  # a data atual como uma variável de contexto para o modelo
    pending_accounts = Transactions.objects.filter(user=user, paid=False, date_transaction__lte=today)
    if pending_accounts.exists():
        message = f'Você possui {pending_accounts.count()} conta(s) com status como Pendente'
        notify_alert = notify.send(user, recipient=user, verb=message)
        return pending_accounts, message, notify_alert
    return None, None, None
