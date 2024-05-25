from django.conf import settings
from django.core.mail import send_mail


def send_email(subject, message, recipients):
    send_mail(
        subject,
        message,
        settings.MAIL_HOST_USER,
        recipients,
        fail_silently=False,
    )
