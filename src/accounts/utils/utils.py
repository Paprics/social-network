# utils.py
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_email_verified}"


def send_registration_email(user, request) -> None:

    uidb64 = urlsafe_base64_encode(force_bytes(user.id))
    token = TokenGenerator().make_token(user)
    domain = get_current_site(request).domain
    activation_link = f"http://{domain}/activate/{uidb64}/{token}/"

    message = render_to_string(
        "activation_email.html",
        {
            "user": user,
            "activation_link": activation_link,
        },
    )

    email = EmailMessage(
        subject="Активація облікового запису",
        body=message,
        to=[user.email],
    )

    email.content_subtype = "html"
    email.send(fail_silently=True)
