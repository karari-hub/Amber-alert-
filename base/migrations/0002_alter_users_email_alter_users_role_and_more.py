# Generated by Django 4.2.6 on 2023-11-02 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='role',
            field=models.CharField(choices=[('C', 'Citizen'), ('P', 'parent'), ('G', 'guardian'), ('LE', 'Law enforcer/police')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]