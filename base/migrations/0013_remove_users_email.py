# Generated by Django 5.0.2 on 2024-02-26 22:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_alter_users_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='email',
        ),
    ]
