from django.shortcuts import render
from django.views.decorators.http import require_GET

from utils.notifications import send_pending_accounts_notification


@require_GET
def notifications(request):
    context = {}
    pending_accounts, message, notify_alert = send_pending_accounts_notification(request.user)
    if pending_accounts is not None:
        context = {
            'notifications': pending_accounts.count(),
            'message': message,
            'notify_alert': notify_alert[0]
        }
    return context


