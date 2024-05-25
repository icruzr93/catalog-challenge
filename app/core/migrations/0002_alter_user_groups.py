# Generated by Django 4.2.13 on 2024-05-24 22:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="groups",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="auth.group",
            ),
        ),
    ]
