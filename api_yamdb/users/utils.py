from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from .models import User
from api_yamdb.settings import ADMIN_EMAIL


def send_confirmation_code(username):
    admin_email = ADMIN_EMAIL
    user = get_object_or_404(User, username=username)
    user_email = [user.email]
    confirmation_code = default_token_generator.make_token(user)
    subject = "Код подтверждения"
    message = f"{confirmation_code} - код для авторизации"
    return send_mail(subject, message, admin_email, user_email)
