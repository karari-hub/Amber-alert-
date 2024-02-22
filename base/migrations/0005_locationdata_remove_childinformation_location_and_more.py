# Generated by Django 4.2.6 on 2023-11-07 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_rename_parent_name_childinformation_parent_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Locationdata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=255, null=True)),
                ('county', models.CharField(max_length=255, null=True)),
                ('district', models.CharField(max_length=255, null=True)),
                ('division', models.CharField(max_length=255, null=True)),
                ('location', models.CharField(max_length=255, null=True)),
                ('sublocation', models.CharField(max_length=255, null=True)),
                ('town', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='childinformation',
            name='location',
        ),
        migrations.RemoveField(
            model_name='missingpersons',
            name='location',
        ),
        migrations.RemoveField(
            model_name='reports',
            name='location',
        ),
    ]