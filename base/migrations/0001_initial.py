# Generated by Django 4.2.6 on 2023-11-02 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alerts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alert_tittle', models.CharField(max_length=255, null=True)),
                ('alert_type', models.CharField(choices=[('Missing_person', 'Missing person'), ('Missing_child', 'Missing child')], max_length=50, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Found', 'Found')], max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChildInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child_name', models.CharField(max_length=255, null=True)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(max_length=50, null=True)),
                ('physical_description', models.TextField()),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('parent_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='MissingPersons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(max_length=50)),
                ('physical_description', models.TextField(max_length=255, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('family_contact', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('bio', models.TextField(blank=True, max_length=255, null=True)),
                ('role', models.CharField(choices=[('C', 'Citizen'), ('P', 'parent'), ('G', 'guardian'), ('LE', 'Law enforcer/police')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Reports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('report_type', models.CharField(choices=[('Missing child', 'Missing child'), ('Missing Person', 'Missing person')], max_length=50)),
                ('report_body', models.TextField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('contact_information', models.CharField(blank=True, max_length=255, null=True)),
                ('police_report_number', models.CharField(max_length=255, null=True)),
                ('child', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.childinformation')),
                ('missing_person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.missingpersons')),
                ('users', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.users')),
            ],
        ),
        migrations.AddField(
            model_name='missingpersons',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.users'),
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('body', models.CharField(blank=True, max_length=255, null=True)),
                ('alerts', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.alerts')),
                ('report', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.reports')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.users')),
            ],
        ),
        migrations.AddField(
            model_name='childinformation',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.users'),
        ),
        migrations.AddField(
            model_name='alerts',
            name='report',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.reports'),
        ),
        migrations.AddField(
            model_name='alerts',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.users'),
        ),
        migrations.CreateModel(
            name='AlertRecipients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alert', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.alerts')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.users')),
            ],
        ),
    ]