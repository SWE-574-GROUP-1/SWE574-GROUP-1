# Generated by Django 4.1.3 on 2023-05-28 22:22

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_alter_profile_background_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmark',
            name='label_name',
            field=models.CharField(default='default', max_length=25),
        ),
        migrations.AddField(
            model_name='profile',
            name='available_labels',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, default=list, size=None),
        ),
        migrations.AlterField(
            model_name='profile',
            name='background_image',
            field=models.ImageField(default='background_images/bg-image-2.jpg', upload_to='background_images'),
        ),
    ]
