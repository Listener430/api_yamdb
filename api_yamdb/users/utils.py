from uuid import uuid4
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from .models import User
from api_yamdb.settings import ADMIN_EMAIL


def send_confirmation_code(username):
    admin_email = ADMIN_EMAIL
    user = get_object_or_404(User, username=username)
    user_email = [user.email]
    confirmation_code = uuid4()
    subject = "Код подтверждения"
    message = f"{confirmation_code} - код для авторизации"
    return send_mail(subject, message, admin_email, user_email)


"""
def code(username):
    user = get_object_or_404(User, username=username)
    confirmation_code = uuid4()
    user.confirmation_code = confirmation_code
    send_mail(
        "Код подтвержения для завершения регистрации",
        f"Ваш код для получения JWT токена {user.confirmation_code}",
        ADMIN_EMAIL,
        [user.email],
        fail_silently=False,
    )
"""
