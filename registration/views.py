from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.views.decorators.http import require_GET

from home import settings
from registration.forms import SignUpForm, UserChangeData


def register_user(request):
    msg = ""
    success = False
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if not form.is_valid():
            msg = 'O formulário não é válido'
        else:
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'Usuário criado com sucesso! <a href="/banks_accounts/login">login</a>.'
            success = True
    else:
        form = SignUpForm()

    return render(request, "registration/register.html", {"form": form, "msg": msg, "success": success})


@login_required
@require_GET
def show_user_profile(request):
    return render(request, 'registration/user_profile.html')


@login_required
def update_profile_data(request, pk):
    if request.method == "POST":
        form = UserChangeData(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect("/user_profile/", messages)
    else:
        form = SignUpForm(instance=request.user)
        context = {'form': form, }
        return render(request, 'registration/update_profile_data.html', context)


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Solicitação de alteração de senha"
                    email_template = "registration/password/password_reset_email.txt"

                    context = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Finans App',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user.first_name,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    html_content = render_to_string(email_template, context=context)
                    text_content = strip_tags(html_content)

                    email_subject = "Alteração da Senha da Central do Assinante"
                    email = EmailMultiAlternatives(
                        email_subject,
                        text_content,
                        from_email=settings.EMAIL_HOST_USER,
                        to=[user.email]
                    )
                    email.attach_alternative(html_content, 'text/html')

                    try:
                        send_mail(subject, text_content, 'Troca de senha', [user.email])
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    
                    return redirect("password_reset/done/")
    password_reset_form = PasswordResetForm()
    context = {"password_reset_form": password_reset_form}
    return render(request=request, template_name="registration/password/password_reset.html", context=context)



