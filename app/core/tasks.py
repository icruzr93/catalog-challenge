from celery import shared_task

from app.core import utils
from app.core.models import User


@shared_task
def on_user_created(id, user_id):
    """Notify admins about the new user"""
    email_list = User.objects.all().values_list("email", flat=True)
    created_by = User.objects.filter(id=user_id).first()
    new_user = User.objects.get(id=id)

    message = f"User '{new_user}' created by '{created_by}'"

    utils.send_email("New user created", message, email_list)
