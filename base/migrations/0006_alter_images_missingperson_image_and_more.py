# Generated by Django 5.0.2 on 2024-03-26 12:26

import base.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_images_alter_alerts_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='missingperson_image',
            field=models.ImageField(blank=True, null=True, upload_to=base.models.upload_to),
        ),
        migrations.AlterField(
            model_name='images',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to=base.models.upload_to),
        ),
    ]
