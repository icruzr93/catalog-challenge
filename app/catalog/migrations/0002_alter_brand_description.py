# Generated by Django 4.2.13 on 2024-05-24 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="brand",
            name="description",
            field=models.CharField(null=True),
        ),
    ]