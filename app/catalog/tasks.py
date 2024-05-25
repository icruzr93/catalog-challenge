from celery import shared_task

from app.catalog.models import Product
from app.core import utils
from app.core.models import User


@shared_task
def on_product_created(product_id, user_id):
    """Notify admins about the new product"""
    email_list = User.objects.all().values_list("email", flat=True)
    new_product = Product.objects.get(id=product_id)
    created_by = User.objects.filter(id=user_id).first()

    message = f"Product '{new_product}' added by '{created_by}'"

    utils.send_email("New product created", message, email_list)


@shared_task
def on_product_updated(product_id, user_id):
    """Notify admins about product updated"""
    email_list = User.objects.all().values_list("email", flat=True)
    created_by = User.objects.filter(id=user_id).first()
    product = Product.objects.get(id=product_id)

    message = f"Product '{product}' modified by '{created_by}'"

    utils.send_email("Product updated", message, email_list)


@shared_task
def on_product_deleted(product_id, user_id):
    """Notify admins about product deleted"""
    email_list = User.objects.all().values_list("email", flat=True)
    created_by = User.objects.filter(id=user_id).first()
    product = Product.objects.get(id=product_id)

    message = f"Product '{product}' deleted by '{created_by}'"

    utils.send_email("Product deleted", message, email_list)
